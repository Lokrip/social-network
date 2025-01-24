"""
Django settings for services project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_peh^$jo3*6*nc2o-eg5bl%nf5#o(h84qg-h0l_00h2@+u)-y2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "172.17.0.1",
    "172.18.0.3"
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'channels',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'django_countries',
    'debug_toolbar',
    'mptt',
    
    'database.apps.DatabaseConfig',
    'home.apps.HomeConfig',
    'account.apps.AccountConfig',
    'slices.apps.SlicesConfig',
    'appSerilizers.apps.AppserilizersConfig',
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,  # Показывать панель всегда
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv('REDIS_CONTAINER_NAME'), 6379)],
        },
    },
}


ROOT_URLCONF = 'services.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context.context_processors.get_context_django'
            ],
        },
    },
]

ASGI_APPLICATION = 'services.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}

AUTH_USER_MODEL = 'database.User'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'



#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'slavadorohov499@gmail.com'
EMAIL_HOST_PASSWORD = 'xzwrtlsyagmmnfir'

#Celery

#Хост редиса
REDIS_HOST = os.getenv('REDIS_CONTAINER_NAME') # Адрес, по которому Redis будет доступен. '0.0.0.0' означает, что Redis будет доступен на всех интерфейсах.
#Порт редиса
REDIS_PORT = '6379' # Порт, на котором Redis будет слушать входящие соединения. 6379 - это стандартный порт для Redis.

#брокер URL
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# Параметры транспорта брокера
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} # Опции для транспорта брокера, где 'visibility_timeout' указывает время (в секундах), в течение которого задача будет недоступна для повторной обработки после получения.
# URL для хранения результатов
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' # URL для хранения результатов выполнения задач, также указывает на Redis и использует ту же базу данных.
# Разрешенные форматы контента
CELERY_ACCEPT_CONTENT = ['application/json'] # Указывает, какие форматы контента Celery может принимать. В данном случае это JSON.
# Сериализатор задач
CELERY_TASK_SERIALIZER = 'json' # Указывает, в каком формате задачи будут сериализованы (преобразованы в строку) перед отправкой в брокер. Здесь используется JSON.
# Сериализатор результатов
CELERY_RESULT_SERIALIZER = 'json'  # Указывает, в каком формате результаты выполнения задач будут сериализованы. В данном случае также используется JSON.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # This can be adjusted to 'ERROR' to reduce verbosity
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'CRITICAL',  # To suppress SQL query logs
            'propagate': False,
        },
    },
}