from django.db import models

from product.models import Product
from userauth.models import User
from customer.models import BillingAddress


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"


class Order(models.Model):
    Order_status = (
        ('Pending', 'Pending'),
        ('In Review', 'In Review'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    Payment = (
        ('Cash', 'Cash'),
        ('bKash', 'bKash'),
        ('Nagad', 'Nagad'),
        ('SSLCOMMERZE', 'SSLCOMMERZE'),
    )

    Payment_Status = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tax = models.DecimalField(max_digits=8, decimal_places=2)
    grand_total = models.DecimalField(max_digits=8, decimal_places=2)
    coupon_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    delivery_status = models.CharField(max_length=11, choices=Order_status, default='Pending')
    payment_method = models.CharField(max_length=12, choices=Payment)
    payment_status = models.CharField(max_length=6, choices=Payment_Status)
    payment_details = models.TextField(null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username}'s Order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.order.user.username}'s Order"
