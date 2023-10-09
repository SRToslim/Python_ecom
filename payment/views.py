import random

import requests
from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pysslcmz.payment import SSLCSession
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem, Order, OrderItem
from coupon.models import CouponUsage
from customer.models import BillingAddress


def cash_on_delivery(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart__user=user)

    sub_total_amount = 0
    total_tax = 0
    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax

    coupon_usages = CouponUsage.objects.filter(user=request.user, coupon=request.session['coupon_id'])
    total_discount_amount = Decimal(0)
    for coupon_usage in coupon_usages:
        total_discount_amount += coupon_usage.discount_amount

    total_price = (sub_total_amount - total_discount_amount) + total_tax

    shipping = BillingAddress.objects.get(user=user)
    order = Order.objects.create(
        user=user,
        shipping_address=shipping,
        total_price=sub_total_amount,
        total_tax=total_tax,
        grand_total=total_price,
        payment_method='Cash',
        delivery_status='Pending',
        payment_status='Unpaid',
        coupon_discount=total_discount_amount,
        note=shipping.note,
        code=str(random.randint(10000000, 99999999))
    )

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
        )

        product = cart_item.product
        product.qty = F('qty') - cart_item.quantity
        product.save()

    order_item = OrderItem.objects.filter(order__id=order.id)

    cart_items.delete()
    cart.delete()

    return render(request, 'cart/order_confirmation.html', {'order': order, 'order_item': order_item})


def sslcommerz_payment(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)

    sub_total_amount = 0
    total_tax = 0
    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax

    coupon_usages = CouponUsage.objects.filter(user=request.user, coupon=request.session['coupon_id'])
    total_discount_amount = Decimal(0)
    for coupon_usage in coupon_usages:
        total_discount_amount += coupon_usage.discount_amount

    total_price = (sub_total_amount - total_discount_amount) + total_tax

    shipping = BillingAddress.objects.get(user=user)

    store_id = 'duron65154d8a6c4b9'
    store_password = 'duron65154d8a6c4b9@ssl'

    # store_id = 'lavendersuperstorecombdlive'
    # store_password = '5E8ADD9705F0F83074'

    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_password)

    status_url = request.build_absolute_uri(reverse(ssl_status))

    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    mypayment.set_product_integration(total_amount=Decimal(total_price), currency='BDT', product_category='grocery',
                                      product_name='product', num_of_item=cart_items.count(),
                                      shipping_method='YES', product_profile='None')

    mypayment.set_customer_info(name=user.profile.full_name, email=user.email, address1=user.profile.address,
                                address2=user.profile.address, city=user.profile.city, postcode=user.profile.zipcode,
                                country=user.profile.country, phone=user.phone)

    mypayment.set_shipping_info(shipping_to=BillingAddress.fname, address=shipping.billing_address, city=shipping.city,
                                postcode=shipping.zipcode, country=shipping.country)

    response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def ssl_status(request):
    if request.method == 'POST':
        payment_data = request.POST
        status = payment_data.get('status')
        if status == 'VALID':

            # val_id = payment_data.get('val_id')
            # tran_id = payment_data.get('tran_id')

            return HttpResponseRedirect(reverse('ssl_payment_success', kwargs={'payment_data': payment_data}))
            # return HttpResponseRedirect(reverse('ssl_payment_success', kwargs={'val_id': val_id, 'tran_id': tran_id}))

        elif status == 'FAILED':
            return HttpResponseRedirect(reverse('ssl_payment_failed'))

        elif status == 'CANCELLED':
            return HttpResponseRedirect(reverse('ssl_payment_cancel'))

    return render(request, 'payment/status.html')


def sslcommerze_payment_success(request, payment_data):
    # return HttpResponse(f"val_id: {val_id}, tran_id: {tran_id}")
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart__user=user)

    sub_total_amount = 0
    total_tax = 0
    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax

    coupon_usages = CouponUsage.objects.filter(user=request.user, coupon=request.session['coupon_id'])
    total_discount_amount = Decimal(0)
    for coupon_usage in coupon_usages:
        total_discount_amount += coupon_usage.discount_amount

    total_price = (sub_total_amount - total_discount_amount) + total_tax

    shipping = get_object_or_404(BillingAddress, user=user)

    order = Order.objects.create(
        user=user,
        shipping_address=shipping,
        total_price=sub_total_amount,
        total_tax=total_tax,
        grand_total=total_price,
        payment_method='SSLCOMMERZE',
        delivery_status='Pending',
        payment_status='Paid',
        payment_details=payment_data,
        coupon_discount=total_discount_amount,
        note=shipping.note,
        code=str(random.randint(10000000, 99999999))
    )

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
        )

        product = cart_item.product
        product.qty = F('qty') - cart_item.quantity
        product.save()

    order_item = OrderItem.objects.filter(order__id=order.id)

    cart_items.delete()
    cart.delete()

    return render(request, 'cart/order_confirmation.html', {'order': order, 'order_item': order_item})


def sslcommerze_payment_failed(request):
    messages.error(request, 'Payment failed.')
    return redirect('checkout')


def sslcommerze_payment_cancel(request):
    messages.warning(request, 'Payment cancel.')
    return redirect('checkout')


def create_bkash_payment(request):
    user = request.user
    # cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart__user=user)

    sub_total_amount = 0
    total_tax = 0
    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax
    total_price = str(sub_total_amount + total_tax)

    url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create"

    payload = {
        "mode": "tokenized",
        "callbackURL": "http://lavendersuperstore.com.bd",
        "payerReference": "1",
        "agreementID": user.phone,
        "amount": total_price,
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": str(random.randint(100000, 999999))
    }

    headers = {
        "accept": "application/json",
        "Authorization": request.session.get('sessionid'),
        "X-APP-Key": "4f6o0cjiki2rfm34kfdadl1eqq",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return redirect('checkout')
