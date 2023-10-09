from django.urls import path

from .views import *

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('update-cart/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('increase/<int:cart_item_id>/', increase, name='increase'),
    path('decrease/<int:cart_item_id>/', decrease, name='decrease'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('place-order/', create_order, name='order_place'),
]