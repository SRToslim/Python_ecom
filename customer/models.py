from django.db import models

from userauth.models import User


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    billing_address = models.CharField(max_length=30)
    billing_address2 = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=15)
    city = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=5)
    phone = models.CharField(max_length=11)
    cname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Billing Address"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=10, null=True, blank=True)
    lname = models.CharField(max_length=10, null=True, blank=True)
    cname = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    shipping_address = models.CharField(max_length=30, null=True, blank=True)
    shipping_address2 = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=10, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Shipping Address"
