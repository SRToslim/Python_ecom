from django.contrib import admin

from .models import *


class HeaderAdmin(admin.ModelAdmin):
    list_display = ['contact', 'image']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'slider', 'active']


class FooterAdmin(admin.ModelAdmin):
    list_display = ['about', 'email', 'mobile']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'is_active']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['text', 'banner', 'is_active']


class OrderValueAdmin(admin.ModelAdmin):
    list_display = ['min_order']


admin.site.register(Header, HeaderAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Order_value, OrderValueAdmin)