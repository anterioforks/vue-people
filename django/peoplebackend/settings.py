"""
Django settings for peoplebackend project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = ['django:8000', 'django', 'localhost', 'vuepeople.pulilab.com', 'www.vuepeople.org', 'vuepeople.org']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'rest_framework',
    'rest_framework_gis',
    'taggit',
    'taggit_serializer',
    'simple-feedback',
    'people'
]

if not DEBUG:
    sentry = os.environ.get('SENTRY_DSN')
    if sentry:
        INSTALLED_APPS += ['raven.contrib.django.raven_compat']
        RAVEN_CONFIG = {
            'dsn': sentry,
        }
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'root': {
                'level': 'WARNING',
                'handlers': ['sentry'],
            },
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s '
                              '%(process)d %(thread)d %(message)s'
                },
            },
            'handlers': {
                'sentry': {
                    'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
                    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                    'tags': {'custom-tag': 'x'},
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'ERROR',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'raven': {
                    'level': 'DEBUG',
                    'handlers': ['sentry', 'console'],
                    'propagate': False,
                },
                'sentry.errors': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
            },
        }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'peoplebackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'peoplebackend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': os.environ.get("DATABASE_URL", 'postgis'),
        'PASSWORD': 'postgres',
        'PORT': 5432,
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # 'rest_framework.permissions.AllowAny'
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication'
    )
}

SOCIALACCOUNT_ADAPTER = 'people.adapter.MyGithubAccountAdapter'
ACCOUNT_ADAPTER = 'people.adapter.MyAccountAdapter'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'read:user',
            'user:email'
        ],
    }
}

LOGIN_REDIRECT_URL = '/user?token={}'
LOGIN_REDIRECT_URL_DEV = 'http://localhost:3000/user?token={}'
