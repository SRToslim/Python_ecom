from django.db import models

from cart.models import Order
from product.models import Product
from userauth.models import User


class Coupon(models.Model):
    objects = None
    DoesNotExist = None
    Discount_Type = (
        ('flat', 'Flat'),
        ('percent', 'Percent'),
    )
    code = models.CharField(max_length=255, unique=True)
    details = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_type = models.CharField(choices=Discount_Type, max_length=7)
    usage_limit = models.PositiveIntegerField(default=1)
    start_date = models.DateTimeField(auto_now_add=False)
    end_date = models.DateTimeField(auto_now_add=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.code

    def total_discount(self, product_price):
        if self.discount_type == 'flat':
            coupon_discount = product_price - self.discount
            return coupon_discount
        else:
            coupon_discount = (self.discount / 100) * product_price
            return coupon_discount


class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    used_count = models.PositiveIntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        # return f"{self.user.username} is use Coupon: {self.coupon.code} on Order: {self.order.code}"
        return f"{self.user.username} is use Coupon: {self.coupon.code}"