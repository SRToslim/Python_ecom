from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from coupon.models import Coupon


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, end_date__gte=timezone.now())
            request.session['coupon_id'] = coupon.id
            # You can add logic to calculate the discount and store it in the session or order.
            return redirect('checkout')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')

    return render(request, 'coupons/apply_coupon.html')