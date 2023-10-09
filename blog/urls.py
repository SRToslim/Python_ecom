from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', all_blog, name='all_blog'),
    path('blog/<slug>', blogDetails, name='blog_details'),
]