from django.urls import path

from .views import *

urlpatterns = [
    path('user/dashboard/', user_dashboard, name='dashboard'),
    path('user/order-history/', CustomerOrder, name='userOrder'),
    path('user/profile/', CustomerInfo, name='userProfile'),
    path('user/address/', customer_address, name='customer_address'),
    path('user/order-details/<int:id>/', orderDetails, name='orderDetails'),
]
