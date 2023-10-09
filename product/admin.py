from django.contrib import admin

from .models import *


class ProductImageAdmin(admin.TabularInline):
    model = ProductImages


class ProductVideoAdmin(admin.TabularInline):
    model = ProductVideo


class ProductVariationAdmin(admin.TabularInline):
    model = VariationValue


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, ProductVideoAdmin, ProductVariationAdmin]
    list_editable = ['qty']
    list_display = [
        'name',
        'product_image',
        'sku',
        'category',
        'qty',
        'price',
        'old_price',
        'discount',
        'offer',
        'cod',
        'featured',
        'status',
    ]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'status']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand_image', 'featured', 'status']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image', 'contact', 'address']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'status', 'created_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Location, LocationAdmin)
