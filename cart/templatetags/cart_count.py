from django import template
from cart.models import Cart
from wishlist.models import WishlistItem

register = template.Library()


@register.simple_tag
def cart_item_count(user):
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.cartitem_set.count()
    return 0


@register.simple_tag
def wishlist_item_count(user):
    if user.is_authenticated:
        return WishlistItem.objects.filter(user=user).count()
    return 0


@register.simple_tag
def mini_cart(user):
    if user.is_authenticated:
        cart = Cart.objects.get(user=user)
        cart_products = cart.cartitem_set.all()[:2]
        products = cart.cartitem_set.all()

        sub_total_amount = 0
        total_tax = 0
        for item in products:
            sub_total_amount += item.quantity * item.product.price
            tax = item.product.tax_price() * item.quantity
            total_tax += tax
        total_amount = sub_total_amount + total_tax

        return cart_products, total_amount
    return 0


@register.filter(name='rating_to_stars')
def rating_to_stars(rating):
    stars = '★' * rating
    empty_stars = '☆' * (5 - rating)
    return f'{stars}{empty_stars}'
