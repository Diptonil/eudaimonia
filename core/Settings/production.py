from .base import *
import django_heroku
import environ


env = environ.Env()
django_heroku.settings(locals())


SECRET_KEY = env('SECRET_KEY')


DEBUG = False


ALLOWED_HOSTS = ['your-mom-s-journal.herokuapp.com']


SESSION_EXPIRE_AT_BROWSER_CLOSE = True


PASSWORD_RESET_TIMEOUT_DAYS = 1


DATABASES = {
    'default': env.db(),
}


ADMINS = ('Batman', 'diptonilr@gmail.com')
MANAGERS = ("Your Mom's Journal", 'yourmomsjournal@gmail.com')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yourmomsjournal@gmail.com'
EMAIL_HOST_PASSWORD = 'sylnklistqsmsztw'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'yourmomsjournal@gmail.com'


RECATCHA_PUBLIC_KEY = '6Lde9vYeAAAAAAqkzxT95WxssHcD_fHb16Jc_EbC'
RECAPTCHA_PRIVATE_KEY = '6Lde9vYeAAAAAK6WbLJOym1TazSq24xej5DZwc9f'


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'


CSP_DEFAULT_SRC = ("'self'", )
CSP_FONT_SRC = ("'self'", )
CSP_CONNECT_SRC = ("'self'", "www.google-analytics.com")
CSP_OBJECT_SRC = ("'self'", )
CSP_BASE_URI = ("'self'", )
CSP_FRAME_ANCESTORS = ("'self'", )
CSP_FORM_ACTION = ("'self'", )
CSP_INCLUDE_NONCE_IN = ('script-src', )
CSP_MANIFEST_SRC = ("'self'", )
CSP_WORKER_SRC = ("'self'", )
CSP_MEDIA_SRC = ("'self'", )
CSP_IMG_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "ajax.cloudflare.com",)
CSP_STYLE_SRC = ("'self'")
