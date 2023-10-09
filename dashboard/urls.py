from django.urls import path
from . views import *

urlpatterns = [
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin/profile/', view_profile, name='profile'),
    path('admin/change-password/', ChangePasswordView.as_view(), name='update_password'),
    path('admin/deactivate-profile/', deactivate_profile, name='deactivate_profile'),
    path('admin/categories/', categories_add_view, name='categories_add_view'),
    path('admin/categories/edit/<str:slug>', categories_edit_view, name='categories_edit_view'),
    path('admin/categories/delete/<str:slug>', delete_category, name='delete_category'),
    path('admin/brand/', brand_view, name='brand_view'),
    path('admin/brand/add', brand_add_view, name='brand_add_view'),
    path('admin/brand/edit/<slug>', brand_edit_view, name='brand_edit_view'),
    path('admin/brand/delete/<str:slug>', delete_brand, name='delete_brand'),
    path('admin/customer-list/', all_customers, name='all_customers'),
    path('admin/deactivate_customer/<int:id>/', deactivate_customer, name='deactivate_customer'),
    path('admin/activate_customer/<int:id>/', activate_customer, name='activate_customer'),
    path('admin/admin-list/', admin_list, name='admin_list'),
    path('admin/deactivate_admin/<int:id>/', deactivate_admin, name='deactivate_admin'),
    path('admin/activate_admin/<int:id>/', activate_admin, name='activate_admin'),
    path('admin/all-staff/', staff_list, name='staff_list'),
    path('admin/deactivate_staff/<int:id>/', deactivate_staff, name='deactivate_staff'),
    path('admin/activate_staff/<int:id>/', activate_staff, name='activate_staff'),
    path('admin/all-order/', admin_panel_order_view, name='all_order'),
    path('admin/vendor-order/', admin_panel_seller_view, name='seller_order'),
    path('admin/order/details/<int:id>', admin_panel_order_details, name='order_details'),
    path('admin/product/review/', admin_panel_product_review, name='review_product'),
]