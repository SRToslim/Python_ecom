from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.safestring import mark_safe


class CustomManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verify', True)
        extra_fields.setdefault('user_type', 'developer')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be is_staff=true')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('superuser must be is_admin=true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be is_superuser=true')
        if extra_fields.get('is_active') is not True:
            raise ValueError('superuser must be is_active=true')
        if extra_fields.get('is_verify') is not True:
            raise ValueError('superuser must be is_verify=true')

        return self.create_user(email, username, password, **extra_fields)


# noinspection PyCompatibility
class User(AbstractBaseUser, PermissionsMixin):
    DoesNotExist = None
    USER_TYPE = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('developer', 'Developer')
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default='customer')
    phone = models.CharField(max_length=14, blank=True, null=True, unique=True)
    membership_no = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')
    last_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='last IP address')
    client_os_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='OS Info')
    client_browser_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='Browser Info')
    client_device_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='Device Info')
    social_id = models.CharField(max_length=255, blank=True, null=True)
    social_provider = models.CharField(max_length=255, blank=True, null=True) 

    objects = CustomManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(f'{self.username}')

    def save(self, *args, **kwargs):
        if self.email:
            user_email = self.email
            if '@' in user_email:
                split_username = user_email.index('@')
                get_username = user_email[:split_username]
                self.username = get_username
            return super().save(*args, **kwargs)
        else:
            user = self.username
            self.username = user
            return super().save(*args, **kwargs)


class Profile(models.Model):
    Gender = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='user/', blank=True, null=True, default='default.png')
    address = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=Gender, blank=True, null=True)
    dob = models.CharField(max_length=10, null=True, blank=True, verbose_name='Date of Birth')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def user_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % self.image.url)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        if self.user.email:
            user_email = self.user.email
            if '@' in user_email:
                split_username = user_email.index('@')
                get_username = user_email[:split_username]
                self.username = get_username
            return super().save(*args, **kwargs)
        else:
            user = self.user.username
            self.username = user
            return super().save(*args, **kwargs)
