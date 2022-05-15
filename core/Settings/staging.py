from .base import *
from os.path import join


DEBUG = False


SECRET_KEY = 'some-random-shit-that-actually-is-hidden'


ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'staging'),
    }
}


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


RECATCHA_PUBLIC_KEY = '6Lde9vYeAAAAAAqkzxT95WxssHcD_fHb16Jc_EbC'