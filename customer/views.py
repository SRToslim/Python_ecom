import io
import json
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View

from cart.models import Order, OrderItem
from helpbazar import settings
from shop_settings.models import Currency
from userauth.models import Profile
from wishlist.models import WishlistItem

from .forms import UpdateUserForm, UpdateProfileForm, BillingAddressForm
from .models import BillingAddress

from .utils import DASHBOARD_TEMPLATE_NAME


@login_required(login_url='login')
def user_dashboard(request):
    prof = Profile.objects.get(user=request.user)
    total_ordered_products_per_user = OrderItem.objects.filter(order__user=request.user).values('order__user').annotate(total_products=Sum('quantity'))
    count = total_ordered_products_per_user[0]['total_products'] if total_ordered_products_per_user else 0
    wishlist = WishlistItem.objects.filter(user=request.user)
    return render(request, DASHBOARD_TEMPLATE_NAME, {'prof': prof, 'count': count, 'wishlist': wishlist})


@login_required(login_url='login')
def CustomerInfo(request):
    prof = Profile.objects.get(user=request.user)
    active = str(prof.user.last_login - prof.date_joined).split('.')[0]

    if request.method == 'POST':
        handle_post_request(request, prof)

    return render(request, 'customer/profile.html', {'prof': prof, 'active': active})


def handle_post_request(request, prof):
    UserForm = UpdateUserForm(request.POST, instance=request.user)
    profileForm = UpdateProfileForm(request.POST, request.FILES, instance=prof)

    if UserForm.is_valid() and profileForm.is_valid():
        user = UserForm.save(commit=False)
        user.save()
        prof = profileForm.save(commit=False)
        if 'image' in request.FILES:
            if request.user.profile.image != 'default.png':
                request.user.profile.image.delete()
                prof.image = request.FILES['image']
            prof.save()
        else:
            prof.save()
        messages.success(request, 'Your profile is updated successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Invalid form data. Please check the inputs.')

    return render(request, 'customer/profile.html')


@login_required(login_url='login')
def customer_address(request):
    prof = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        saved_address = BillingAddress.objects.get(user=request.user)
        billingForm = BillingAddressForm(request.POST, instance=saved_address)

        if billingForm.is_valid():
            billing = billingForm.save(commit=False)
            billing.user = request.user
            billing.save()

            messages.success(request, f'Address is successfully save.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, f'Invalid Form')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        saved_address, _ = BillingAddress.objects.get_or_create(user=request.user)
        billing_form = BillingAddressForm(instance=saved_address)

        return render(request, 'customer/address.html', {'prof': prof, 'form': billing_form})


@login_required(login_url='login')
def CustomerOrder(request):
    prof = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    item_per_page = 8
    paginator = Paginator(orders, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'prof': prof,
        'page': page
    }
    return render(request, 'customer/order.html', context)


def orderDetails(request, id):
    order = Order.objects.get(pk=id)

    order_item = OrderItem.objects.filter(order__id=id)

    context = {
        'order': order,
        'order_item': order_item,
    }

    return render(request, 'customer/order-details.html', context)