from django.contrib import admin

from coupon.models import Coupon, CouponUsage

admin.site.register(Coupon)
admin.site.register(CouponUsage)