from pathlib import Path
from os.path import join
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'K*OTkno5c:9ucHVcD)KweRl9k+MLd^>Q`o`kIu)OzWeB_fFAJ_):X.fM`E^q*H^KxeJ</v|$P@CucTJVUb~3S6F@p/-:D*<x"eG*'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '34.135.53.189','34.122.26.110','*']

# Admins are notified by email of request and security issues, in production.
ADMINS = [('Batman', 'diptonilr@gmail.com')]
# Managers are notified by email of broken links and 404 errors, in production.
MANAGERS = [("Your Mom's Journal", 'yourmomsjournal@gmail.com')]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'cloudinary_storage',
    'cloudinary',
    'authentication',
    'journal',
    'dashboard',
    'analysis',
    'APIApp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'journal.views.journal_navbar'
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eudaimonia',
        'USER': 'postgres',
        'PASSWORD': "ITA-H%p>=sN8\*)'",
        'HOST': '34.135.53.189',
        'PORT': '5432'
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

LOGGERS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'format': 'main_formatter'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'dev.log',
            'format': 'main_formatter'
        }
    },
    'loggers': {
        'main': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
        'main': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True
        }
    },
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = (join(BASE_DIR, 'static'),)
STATIC_ROOT = join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'diptonilr@gmail.com'
EMAIL_HOST_PASSWORD = 'esanrubdukrphany'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'diptonilr@gmail.com'

CLOUDINARY_STORAGE = {'CLOUD_NAME': "yourmomscloud", 'API_KEY': "471845542247137", 'API_SECRET': "Jgai2VdgvE1j0hrcnNlgAciPXkA"}
MEDIA_URL = 'media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CELERY_BROKER_URL = 'amqps://vomcxylc:L9uD-DWsO9vwcMqyF7b3CfvqD1F1cudz@puffin.rmq2.cloudamqp.com/vomcxylc'
CELERY_RESULT_BACKEND = 'amqps://vomcxylc:L9uD-DWsO9vwcMqyF7b3CfvqD1F1cudz@puffin.rmq2.cloudamqp.com/vomcxylc'

RECATCHA_PUBLIC_KEY = '6Lde9vYeAAAAAAqkzxT95WxssHcD_fHb16Jc_EbC'
RECAPTCHA_PRIVATE_KEY = '6Lde9vYeAAAAAK6WbLJOym1TazSq24xej5DZwc9f'

'''
sentry_sdk.init(
    dsn="https://d7756c60fa4245ac8057a723bb810f7d@o1249277.ingest.sentry.io/6410159",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
'''
