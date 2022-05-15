from .base import *
from os.path import join
import sys


DEBUG = True


SECRET_KEY = 'some-random-shit-that-actually-is-hidden'


ALLOWED_HOSTS = ['127.0.0.1']


SESSION_EXPIRE_AT_BROWSER_CLOSE = True


PASSWORD_RESET_TIMEOUT_DAYS = 1


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hxoiluux',
        'USER': 'hxoiluux',
        'PASSWORD': 'spo2lr4cZp2m2QNNDlrSudXFVuXrkxwT',
        'HOST': 'john.db.elephantsql.com',
        'PORT': '5432',
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': join(BASE_DIR, 'test'),
        }
    }
}


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yourmomsjournal@gmail.com'
EMAIL_HOST_PASSWORD = 'sylnklistqsmsztw'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'yourmomsjournal@gmail.com'


RECATCHA_PUBLIC_KEY = '6Lde9vYeAAAAAAqkzxT95WxssHcD_fHb16Jc_EbC'
RECAPTCHA_PRIVATE_KEY = '6Lde9vYeAAAAAK6WbLJOym1TazSq24xej5DZwc9f'