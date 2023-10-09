from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from product.models import Product
from wishlist.models import WishlistItem


@login_required(login_url='login')
def WishlistView(request):
    wishlist_item = WishlistItem.objects.filter(user=request.user)

    return render(request, 'wishlist/wishlist-product.html', {'wishlist_item': wishlist_item})


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    WishlistItem.objects.create(user=request.user, product=product)
    messages.success(request, 'Item added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = WishlistItem.objects.get(id=wishlist_item_id)
    wishlist_item.delete()
    messages.success(request, 'Item removed from wishlist.')
    return redirect(request.META.get('HTTP_REFERER'))
