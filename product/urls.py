from django.urls import path

from .views import *

urlpatterns = [
    path('admin/products/', product_list, name='product_list'),
    path('admin/products/add', add_product, name='add_product'),
    path('admin/products/bulk_product_upload', bulk_product_upload, name='bulk_product_upload'),
    path('admin/products/edit/<slug>/', edit_product, name='edit_product'),
    path('admin/products/delete/<slug>/', delete_product, name='delete_product'),
]