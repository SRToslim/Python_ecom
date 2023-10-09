from django.urls import path
from . views import *

urlpatterns = [
    path('contact-us/', contactUs, name='contact_us'),
]