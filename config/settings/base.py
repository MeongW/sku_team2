"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json

from django.core.exceptions import ImproperlyConfigured

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = BASE_DIR / 'secrets.json'
with open(secret_file) as file:
    secrets = json.loads(file.read())

def get_secret(setting, secrets_dict=secrets):
    try:
        return secrets_dict[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')

# SMS_NAVER_SECRET
SMS_NAVER_ACCESS_KEY_ID = get_secret('SMS_NAVER_ACCESS_KEY_ID')
SMS_NAVER_SECRET_KEY = get_secret('SMS_NAVER_SECRET_KEY')
SMS_NAVER_SERVICE_ID = get_secret('SMS_NAVER_SERVICE_ID')
SEND_PHONE_NUMBER = get_secret('SEND_PHONE_NUMBER')

# NAVER_SECRET
NAVER_CLIENT_ID = get_secret('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = get_secret('NAVER_CLIENT_SECRET')

# KAKAO_SECRET
KAKAO_REST_API_KEY = get_secret('KAKAO_REST_API_KEY')
KAKAO_CLIENT_ID = get_secret('KAKAO_CLIENT_ID')
KAKAO_CLIENT_SECRET = get_secret('KAKAO_CLIENT_SECRET')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'posts',
    'accounts',
]

THIRD_PARTY_APPS = [
    # Rest API
    'rest_framework',
    
    
    # User Login, Registration
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    
    # swagger
    'drf_yasg',
    
    # cors
    'corsheaders',

    # ckeditor
    'ckeditor',
    'ckeditor_uploader',

    #django filter
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'





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

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'


# JWT setting
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    
    'TOKEN_USER_CLASS': 'accounts.CustomUser',
}


# dj_rest_auth setting
REST_AUTH = {
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
    'REGISTER_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny', 'accounts.permissions.IsSMSAuthenticated'), 
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': 'accounts.serializers.CustomPasswordResetSerializer',
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_COOKIE': 'access',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_COOKIE_SAMESITE': 'None',
    'JWT_AUTH_COOKIE_DOMAIN': '.servicetori.site',
    'JWT_AUTH_RETURN_EXPIRATION': True,
    'JWT_AUTH_COOKIE_USE_CSRF' : False,
    'SESSION_LOGIN': False,
}
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

SITE_ID = 1
REST_USE_JWT = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'

ACCOUNT_EMAIL_VERIFICATION = 'none'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=False
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_ADAPTER = 'accounts.adapters.CustomSocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': KAKAO_CLIENT_ID,
            'secret': KAKAO_CLIENT_SECRET,
        }
    },
    'naver': {
        'APP': {
            'client_id': NAVER_CLIENT_ID,
            'secret': NAVER_CLIENT_SECRET
        }
    }
}


# cors setting
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://servicetori.site',
    'https://api.servicetori.site',
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://servicetori.site',
    'https://api.servicetori.site',
]


# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
