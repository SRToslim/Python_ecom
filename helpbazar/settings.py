import os
from pathlib import Path

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--jnd5p6^rvvq!-e6-+#xv6^(5f51w05@wupks=upkoc)5kyh^2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom App
    'userauth',
    'shop',
    'product',
    'shop_settings',
    'customer',
    'cart',
    'contact_us',
    'otplogin',
    'payment',
    'dashboard',
    'wishlist',
    'chatbox',
    'blog',
    'coupon',

    # Third-party App
    'fontawesomefree',
    'ckeditor',
    'taggit',
    'active_link',
    'sslserver',
    'ipware',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpbazar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.default',
            ],
        },
    },
]

WSGI_APPLICATION = 'helpbazar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'helpbazar_bd',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'USER': 'helpbazar_bd',
#         'PASSWORD': '@Dhaka@1216+@',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/srtoslim/@tkbd@/use/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AUTH_USER_MODEL = 'userauth.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'support@helpbazar.com'
EMAIL_HOST_USER = 'srtoslim@gmail.com'
EMAIL_HOST_PASSWORD = 'yauwavpnsreektgr'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = [
    'userauth.backend.UsernameOrEmail',
]

# GOOGLE_AUTH_KEY = '28778066899-he4b7r0d92p19nhsdleqoeuiqcffbmuv.apps.googleusercontent.com'
# GOOGLE_AUTH_SECRET = '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'

GOOGLE_AUTH_KEY = '1063760441210-0272bflgivr35lm9l2c87oc9t8ft6qhl.apps.googleusercontent.com'
GOOGLE_AUTH_SECRET = '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'
GOOGLE_AUTH_REDIRECT_URI = 'https://127.0.0.1:8000/auth/google/callback/'

FACEBOOK_APP_ID = '174974117060495'
FACEBOOK_APP_SECRET = '78849958d04f2a3e84f67110e9ada435'
FACEBOOK_REDIRECT_URI = 'https://127.0.0.1:8000/auth/facebook/callback/'

GITHUB_CLIENT_ID = '659d1e258ab02595631e'
GITHUB_CLIENT_SECRET = 'ef378b4612b77ae54ed8126f23065243e2a71d73'
GITHUB_REDIRECT_URI = 'https://127.0.0.1:8000/auth/github/callback/'
# GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
# GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
# GITHUB_USER_URL = 'https://api.github.com/user'

SMS_API_TOKEN = 'jh0fiy2s-gdgcf1ui-5sk0ungx-3spvr5ml-1dnofs8z'
SMS_SID = 'LAVENDERAPI'
SMS_URL = 'https://smsplus.sslwireless.com/api/v3/send-sms/dynamic/'

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'all',
    }
}

JAZZMIN_SETTINGS = {
    'site_title': 'HelpBazar',
    'site_header': 'HelpBazar',
    'site_brand': 'HelpBazar',
    'site_logo': 'favicon.png',
    'login_logo': 'login-logo.png',
    'site_logo_classes': 'img-circle',
    'site_icon': 'favicon.png',
    'copyright': ' - <a href="https://github.com/srtoslim" target="_blank">SRToslim</a>',
    'user_avatar': 'user.image.url',
    'topmenu_links': [
        {'name': 'Home',  'url': 'admin:index'},
        {'name': 'Website', 'url': 'https://127.0.0.1:8000/', 'new_window': True},
        {'model': 'userauth.User'},
        {'app': 'product'},
    ],
    'search_model': 'userauth.User',
    'welcome_sign': 'Welcome to Helpbazar',
    'use_google_fonts_cdn': True,
    'icons': {
        'auth.group': 'fas fa-users-cog',
        'taggit.tag': 'fas fa-tag',
        'userauth.profile': 'far fa-id-badge',
        'userauth.user': 'fas fa-users',
        'product.brand': 'fas fa-registered',
        'product.category': 'far fa-copyright',
        'product.product': 'fab fa-product-hunt',
        'product.vendor': 'fas fa-people-arrows',
        'product.location': 'fas fa-map',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'usermenu_links': [
        {'name': 'Support', 'url': 'https://github.com/srtoslim', 'new_window': True},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "accent": "accent-info",
    "navbar_fixed": True,
    "footer_fixed": True,
    # "sidebar_fixed": True,
}

SSL_ENABLED = True
SSL_CERTIFICATE = 'static/cert.pem'
SSL_KEY = 'static/key.pem'

# FIREBASE_CONFIG = {
#     'apiKey': 'AIzaSyBUUEVkde2ZHveKUmE1e92wfThJn3gZdKY',
#     'authDomain': 'helpbazar.firebaseapp.com',
#     'databaseURL': 'https://helpbazar-default-rtdb.asia-southeast1.firebasedatabase.app',
#     'projectId': 'helpbazar',
#     'storageBucket': 'helpbazar.appspot.com',
#     'messagingSenderId': '28778066899',
#     'appId': '1:28778066899:web:fee32e7687fbeb594c3526',
#     'measurementId': 'G-T40XWEV0DC'
# }

# SSLCommerz Settings
# SSLCOMMERZ_STORE_ID = 'your_store_id'
# SSLCOMMERZ_STORE_PASSWORD = 'your_store_password'
# SSLCOMMERZ_IS_SANDBOX = True
# SSLCOMMERZ_SUCCESS_URL = '/payment/success/'
# SSLCOMMERZ_FAILED_URL = '/payment/failed/'
# SSLCOMMERZ_CANCEL_URL = '/payment/cancel/'
# SSLCOMMERZ_IPN_URL = '/payment/ipn/'
