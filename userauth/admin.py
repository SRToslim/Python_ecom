from django.contrib import admin
from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['social_id', 'social_provider', 'ip', 'last_ip', 'client_os_info', 'client_browser_info', 'client_device_info', 'password', 'last_login']
    # list_editable = ['user_type']
    list_display = ['username', 'email', 'phone', 'user_type', 'is_active', 'is_verify', 'last_ip', 'last_login', 'client_os_info', 'client_browser_info']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_image', 'address', 'dob', 'date_joined', 'city', 'country']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
