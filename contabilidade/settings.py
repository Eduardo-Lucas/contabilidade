"""
Django settings for contabilidade project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(jyrb1zr5e3&bh&fbj0jf%4u57r7p@aoy^)ti-o#q+^7cis_ff'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'usesoft-saas.com', 'comercialtoes-saas.com', 'oleobahia-saas.com']

LOGOUT_REDIRECT_URL = 'index'
LOGIN_REDIRECT_URL = 'index'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_URL = 'login'


# Application definition
SHARED_APPS = (
    # mandatory, should be before any django app
    'tenant_schemas',

    # you must list the app where your tenant models resides in
    'clientes',

    # everything below here is optional
    'glb',
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

)

TENANT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # your tenant specific apps
    'accounts',
    'choices',
    'ctb',
    'glb',

)

INSTALLED_APPS = (
    'tenant_schemas',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',

    'widget_tweaks',

    'accounts',
    'choices',
    'clientes',
    'ctb',
    'glb',

)

# During development only

TENANT_MODEL = 'clientes.Cliente'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    # 'tenant_schemas.middleware.SuspiciousMiddleware',
    # 'tenant_schemas.middleware.DefaultMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contabilidade.urls'

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
            ],
        },
    },
]


WSGI_APPLICATION = 'contabilidade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'tenant_schemas.postgresql_backend',

        # Or path to database file if using sqlite3.
        'NAME': 'contabilidade',

        'USER': 'postgres',
        'PASSWORD': 'usesoft2017#',

        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'HOST': 'localhost',

        # Set to empty string for default
        'PORT': '',
    }

}

DATABASE_ROUTERS = {
    'tenant_schemas.routers.TenantSyncRouter'
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


LOGGING_CONFIG = None


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt_br'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','

DATE_INPUT_FORMATS = [
    '%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y',  # '17-10-2017', '17/10/2017', '17/10/17'
    '%d%m%Y', '%d%m%y',  # '23102017', '231017'
    '%Y-%m-%d', '%Y%m%d',  # '2017-10-23', '20171023'
    '%d %b %Y', '%d de %b de %Y',  # '25 Oct  2006', '25 de Oct de 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d de %B de %Y',  # '17 de October de 2006',
]

DATETIME_INPUT_FORMATS = [
    '%d-%m-%Y %H:%M:%S',
    '%d-%m-%Y %H:%M:%S.%f',
    '%d-%m-%Y %H:%M',
    '%Y-%m-%d', '%Y%m%d',  # '2017-10-23', '20171023'
    '%d-%m-%Y',
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M:%S.%f',
    '%d/%m/%Y %H:%M',
    '%d/%m/%Y',
    '%d/%m/%y %H:%M:%S',
    '%d/%m/%y %H:%M:%S.%f',
    '%d/%m/%y %H:%M',
    '%d/%m/%y']

DATE_FORMAT = 'd/m/Y'
SHORT_DATE_FORMAT = 'd/m/Y'


# DATE_INPUT_FORMATS = [
#     '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
#     '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
#     '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
#     '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
#     '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
# ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
