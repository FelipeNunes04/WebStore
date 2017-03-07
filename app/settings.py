# coding: utf-8
from os import path as os_path

DEFAULT_FROM_EMAIL = 'contato@virtuallia.com.br'
DEFAULT_TO_EMAIL = 'emailvirtuallia@gmail.com'
#CONTACT_EMAIL = 'aguirres@wqti.com.br'
CONTACT_EMAIL = 'virtuallia@gmail.com'
FINANCIAL_EMAIL = 'virtuallia.financeiro@gmail.com'

SITE_NAME = 'Virtuallia'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Renato', 'renatopedigoni@gmail.com'),
    ('Aguirres', 'aguirres@wqti.com.br'),
    ('Rafael', 'rafabmartins@gmail.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

PROJECT_PATH = os_path.abspath(os_path.split(__file__)[0])

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_L10N = False
MEDIA_ROOT = os_path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os_path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    os_path.join(PROJECT_PATH, '../static'),
)

DATE_INPUT_FORMATS = ('%d/%m/%Y', '%d-%m-%Y')
# MODELTRANSLATION_TRANSLATION_REGISTRY = 'translation'

# gettext = lambda s: s
LANGUAGES = (
    ('pt', u'Portuguese'),
    ('en', u'English'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '38-0qwh56b)xy$pes=d5g+3n7%0rjw@fvs1^nevcm(xzqoocj7'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'city_middleware.middleware.DefineCity',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os_path.join(PROJECT_PATH, 'templates'),
)

INTERNAL_IPS = ('127.0.0.1')


INSTALLED_APPS = (
    # django contribs
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.humanize',


    # 3rd party apps
    'debug_toolbar',
    'easy_thumbnails',
    'south',
    'taggit',

    # project apps
    'ads',
    'appsite',
    'banner',
    'channel',
    'city_middleware',
    'contact',
    'category',
    'customer',
    'haystack',
    'locations',
    'news',
    'pagination',
    'payment',
    'polls',
    'voucher',
    'wqti_util',
    # 'zipcode',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

try:
    from local_settings import *
except ImportError:
    print u'Warning: local_settings not found'


DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

AUTH_PROFILE_MODULE = 'customer.UserProfile'

LOGIN_URL = '/cliente/login/'

LOGIN_REDIRECT_URL = "/"


HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = 'whoosh_index'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os_path.join(PROJECT_PATH, 'whoosh_index'),
    },
}
