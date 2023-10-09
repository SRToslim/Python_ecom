from django.contrib import admin

from cart.models import Cart, CartItem, Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['payment_details', 'code']
    list_editable = ['payment_status', 'delivery_status']
    list_display = [
        'user',
        'code',
        'total_price',
        'total_tax',
        'grand_total',
        'payment_method',
        'payment_status',
        'delivery_status',
    ]


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
