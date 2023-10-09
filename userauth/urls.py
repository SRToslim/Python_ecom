from django.urls import path

from .views import login_view, register_view, logout_view, activate, password_reset_request, password_reset_confirm

urlpatterns = [
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]