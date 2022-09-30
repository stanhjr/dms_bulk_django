"""
Django settings for dms_bulk_django project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

SITE_ID = 1

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d!-(1nhmudak$)kxvf(9@2(%r(l2np(n_bl^!eo#yqc8e(yenp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
AUTH_USER_MODEL = 'account.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework',
    'admin_reorder',
    'mathfilters',
    'djstripe',
    'online_users',
    'paypal.standard.ipn',
    'home',
    'account',
    'account_auth',
    'dashboard',
    'order',
    'blog',
    'payment',
    'analytics',
    'important_info'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'online_users.middleware.OnlineNowMiddleware',
]

ROOT_URLCONF = 'dms_bulk_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dms_bulk_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]
# }

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/home/static')
MEDIA_URL = 'media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


ADMIN_REORDER = (
    'sites',
    {'app': 'account', 'label': 'Accounts', 'models': ('account.CustomUser',)},
    {'app': 'blog', 'models': ('blog.ArticleModel',)},
    {'app': 'order', 'label': 'Board Settings', 'models': ('order.BoardModel', 'order.ServicesUnderMaintenance')},
    {'app': 'order', 'models': ('order.OrderCalcModel', 'order.OrderModel')},
    {'app': 'order', 'label': 'Coupons', 'models': ('order.Coupon',)},
    {'app': 'order', 'label': 'Invoices', 'models': ('payment.Invoice',)},
    {'app': 'analytics', 'models': ('analytics.Analytics',)},
    {'app': 'important_info', 'label': 'Frequently Asked Questions', 'models': ('important_info.FAQModel',)},
    {'app': 'home', 'models': ('home.PageModel',)},
    {'app': 'important_info', 'label': 'Seo', 'models': ('important_info.PageModel',)},
)
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "helloworldbooo@gmail.com"
EMAIL_HOST_PASSWORD = "uruqokrnqemmfsne"
CELERY_SEND_MAIL_HOST = "http://185.65.245.191/"

INVALID_DISCOUNT_MESSAGE = 'the entered discount value does not match the actual value mommy hacker'
INVALID_ORDER_AMOUNT_MESSAGE = 'the entered order amount value does not match the actual value mommy hacker'

STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY",
                                        'pk_test_51Lg4MyK6rkKpcwrpM9imgTsK4IupHl9BSeuzPgUQRWExpYnqHxr3Xe9juCUXGR10JXsiknlxoUeZGpTTw2lGG1UF00K0cn1Xv4')
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY",
                                        'STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY')
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY",
                                        'pk_test_51Lg4MyK6rkKpcwrpM9imgTsK4IupHl9BSeuzPgUQRWExpYnqHxr3Xe9juCUXGR10JXsiknlxoUeZGpTTw2lGG1UF00K0cn1Xv4')
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY",
                                        'sk_test_51Lg4MyK6rkKpcwrpBVyS7DCMIIiJxhxDwpCH5ufEg3MPS8QnZtcp3amLtQR5n5lQ1JKO4OVciqPL1K7kJguJZNUS005MqWi0jt')
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = "whsec_QE3hbunXD3fpyvtkc1S1AORm39FzKbEp"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "sb-ea43qt18063883@business.example.com"
PAYPAL_CLIENT_ID = 'ARv3ot_OU4zgMCM_vZ3Xgb0c0ovmFfL_pRRrIlLxPWuq7nZMUUvO2PHS9cCoa1eYNt9G1apgJxyUwqbr'
try:
    from .local_settings import *
except ImportError:
    pass
