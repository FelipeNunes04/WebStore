SITE_URL = 'http://localhost:8000/' # add trailing slash

DEFAULT_FROM_EMAIL = 'aguirres@wqti.com.br'
DEFAULT_TO_EMAIL = 'aguirres@wqti.com.br'
CONTACT_EMAIL = 'aguirres@wqti.com.br'
FINANCIAL_EMAIL = 'aguirres@wqti.com.br'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite3',                   # Or path to database file if using sqlite3.
        'USER': '',                         # Not used with sqlite3.
        'PASSWORD': '',                 # Not used with sqlite3.
        'HOST': 'localhost',                     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                     # Set to empty string for default. Not used with sqlite3.
    }
}
CACHE_BACKEND = 'dummy://'
DEFAULT_FROM_EMAIL = 'wqti.dev@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wqti.dev@gmail.com'
EMAIL_HOST_PASSWORD = 'wd223640'
EMAIL_USE_TLS = True
EMAIL_HOST_PORT = 587
