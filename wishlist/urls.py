from django.urls import path
from wishlist.views import *

urlpatterns = [
    path('wishlist/', WishlistView, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]