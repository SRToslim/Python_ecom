from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from decimal import Decimal

from cart.models import *
from product.models import Product
from shop_settings.models import Order_value
from customer.forms import BillingAddressForm
from customer.models import BillingAddress

from coupon.models import Coupon, CouponUsage


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    sub_total_amount = 0
    total_tax = 0

    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax

    if request.method == 'POST':
        coupon_code = request.POST.get('Coupon')
        try:
            coupon = Coupon.objects.get(code=coupon_code, end_date__gte=timezone.now())

            if CouponUsage.objects.filter(user=request.user, coupon=coupon, used_count__gte=coupon.usage_limit).exists():
                messages.error(request, 'Coupon usage limit reached.')
            else:
                discount = 0
                for item in cart_items:
                    if item.product.old_price is None and item.product.offer != 'today_deal' and item.product.offer != 'Savings' and item.product.offer != 'buy1get1':
                        price_after_discount = item.product.price - coupon.total_discount(item.product.price)

                        item_discount_amount = (item.product.price - price_after_discount) * item.quantity

                        discount += item_discount_amount

                total_discount_amount = discount

                coupon_usage, created = CouponUsage.objects.get_or_create(user=request.user, coupon=coupon, discount_amount=total_discount_amount)
                coupon_usage.used_count += 1
                coupon_usage.save()

                request.session['coupon_id'] = coupon.id
                messages.success(request, 'Coupon applied successfully!')
                return redirect('cart')

        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')

    coupon_usages = CouponUsage.objects.filter(user=request.user, coupon=request.session['coupon_id'])
    total_discount_amount = Decimal(0)
    for coupon_usage in coupon_usages:
        total_discount_amount += coupon_usage.discount_amount
    total_amount = (sub_total_amount - total_discount_amount) + total_tax

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'sub_total_amount': sub_total_amount,
        'tax': total_tax,
        'total_amount': total_amount,
        'total_discount_amount': total_discount_amount,
    })


@login_required(login_url='login')
def increase(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def decrease(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.quantity -= 1
    cart_item.save()
    if cart_item.quantity < 1:
        cart_item.delete()
        return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])


# @login_required(login_url='login')
# def update_cart(request, cart_item_id):
#     cart_item = CartItem.objects.get(pk=cart_item_id)
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity'))
#         if quantity > 0:
#             cart_item.quantity = quantity
#             cart_item.save()
#             messages.success(request, 'Cart update successfully.')
#
#     return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()

    coupon_usages = CouponUsage.objects.filter(user=request.user, coupon=request.session['coupon_id'])

    for coupon_usage in coupon_usages:
        coupon_usage.used_count = 0
        coupon_usage.discount_amount = 0
        coupon_usage.delete()

    if coupon_usages:
        messages.success(request, 'Remove product from cart successfully and coupon removed.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'Remove product from cart successfully.')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def clear_cart(request):
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    user_cart_items = CartItem.objects.filter(cart=cart)
    user_cart_items.delete()
    cart.delete()
    messages.success(request, 'Product delete successfully.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
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

    total_amount = (sub_total_amount - total_discount_amount) + total_tax

    saved_address, _ = BillingAddress.objects.get_or_create(user=user)
    form = BillingAddressForm(instance=saved_address)

    context = {
        'cart_items': cart_items,
        'sub_total_amount': sub_total_amount,
        'tax': total_tax,
        'total_amount': total_amount,
        'form': form
    }

    return render(request, 'cart/checkout.html', context)


@login_required(login_url='login')
def create_order(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)

    sub_total_amount = 0
    total_tax = 0
    for item in cart_items:
        sub_total_amount += item.quantity * item.product.price
        tax = item.product.tax_price() * item.quantity
        total_tax += tax

    if cart_items.exists():
        min_order = Order_value.objects.first()
        if sub_total_amount >= min_order.min_order:
            if request.method == 'POST' or request.method == 'post':
                saved_address = BillingAddress.objects.get(user=user)
                billingForm = BillingAddressForm(request.POST, instance=saved_address)

                if billingForm.is_valid():
                    billing = billingForm.save(commit=False)
                    billing.user = request.user
                    billing.save()
                else:
                    messages.error(request, f'Invalid Form')
                    return redirect(request.META.get('HTTP_REFERER'))

                payment_method = request.POST.get('payment_method')

                if payment_method == 'Cash':
                    return redirect('cash')
                elif payment_method == 'bKash':
                    return redirect('bkash_payment')
                elif payment_method == 'Nagad':
                    pass
                elif payment_method == 'SSLCOMMERZE':
                    return redirect('ssl_payment')
                else:
                    messages.warning(request, "Must select Payment")
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, f"Minimum order value is {min_order.min_order} Taka.")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "Your cart is empty.")
        return redirect(request.META.get('HTTP_REFERER'))
