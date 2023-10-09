from django.urls import path
from payment.views import *

urlpatterns = [
    path('payment/cash/', cash_on_delivery, name='cash'),
    path('payment/', sslcommerz_payment, name='ssl_payment'),
    path('payment/status/', ssl_status, name='ssl_status'),
    path('payment/success/<payment_data>', sslcommerze_payment_success, name='ssl_payment_success'),
    path('payment/failed/', sslcommerze_payment_failed, name='ssl_payment_failed'),
    path('payment/cancel/', sslcommerze_payment_cancel, name='ssl_payment_cancel'),
    path('payment/bkash/', create_bkash_payment, name='bkash_payment'),
]