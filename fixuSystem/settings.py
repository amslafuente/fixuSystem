"""
Django settings for fixuSystem project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from .secrets import SECRET_KEY_PROD
from .secrets import DB_USR, DB_PASSWD
from .secrets import EMAIL_USR, EMAIL_PASSWD

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY_PROD



##### CHANGES FOR PRODUCION ENVIRONMENT #####

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.*']

#############################################



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ###############
    'home_page',
    'gestion_login',
    'gestion_pacientes',
    'gestion_clinica',
    'gestion_citas',
    'gestion_consultas',
    'fixu_estadisticas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fixuSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                ###############
                'home_page/templates',
                'gestion_login/templates',
                'gestion_pacientes/templates',                
                'gestion_clinica/templates',
                'gestion_citas/templates',
                'gestion_consultas/templates',
                'fixu_estadisticas/templates',

            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ###############
                'fixuSystem.context_procs.get_prog_vers',
                'fixuSystem.context_procs.get_datos_clinica',

            ],
        },
    },
]

WSGI_APPLICATION = 'fixuSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'fixuDB',
        'USER':     DB_USR,
        'PASSWORD': DB_PASSWD,
        'HOST':     'localhost',
        'PORT':     '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT =   ['%d/%m/%Y',    # 25/10/2006
                 '%d-%m-%Y',    # 25-10-2006
                 '%Y/%m/%d',    # 2006/10/25
                 '%Y-%m-%d']    # 2006-10-25

TIME_FORMAT = ['%H:%M']

DATE_TIME_FORMAT = ['%d/%m/%Y %H:%M',
                    '%d-%m-%Y %H:%M',
                    '%Y/%m/%d %H:%M',
                    '%Y-%m-%d %H:%M']

##### Login y logout URL #####

LOGIN_URL = '/fixuSystem/access/login/'
LOGOUT_REDIRECT_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expiration on close
SESSION_COOKIE_AGE = 3600 # User logs out after 60 minutes (3600 secs) of inactivity but...
SESSION_SAVE_EVERY_REQUEST = True # timer may be reset in every request

##### Servidores de correo #####

EMAIL_HOST = 'smtp.mydomain.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_USR
EMAIL_HOST_PASSWORD = EMAIL_PASSWD
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
