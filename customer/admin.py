from django.contrib import admin

from customer.models import BillingAddress, ShippingAddress

admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
