from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', include('userauth.urls')),
    path('', include('shop.urls')),
    path('', include('customer.urls')),
    path('settings/', include('shop_settings.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('cart.urls')),
    path('', include('otplogin.urls')),
    path('', include('sociallogin.urls')),
    path('', include('payment.urls')),
    path('', include('dashboard.urls')),
    path('', include('product.urls')),
    path('', include('wishlist.urls')),
    path('', include('contact_us.urls')),
    path('', include('chatbox.urls')),
    path('', include('blog.urls')),
    path('', include('coupon.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)