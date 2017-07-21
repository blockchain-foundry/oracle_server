"""
Django settings for oracle project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# environ setting
root = environ.Path(__file__) - 3  # three folder back
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
env.read_env(str(root.path('.env')))

SERVER_CONFIG_ENV = env("SERVER_CONFIG_ENV")
SECRET_KEY = env("SECRET_KEY")
OSS_API_URL = env("OSS_API_URL")
ORACLE_API_URL = env("ORACLE_API_URL")
CONFIRMATION = env("CONFIRMATION")

DATABASES = {
    "default": {
        "NAME": env("ORACLE_DB"),
        "ENGINE": "django.db.backends.mysql",
        "HOST": env("MYSQL_HOST"),
        "PORT": env("MYSQL_PORT"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_PASSWORD"),
        "OPTIONS": {
            "autocommit": True
        }
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=["*"])
if len(ALLOWED_HOSTS) == 0:
    ALLOWED_HOSTS = ["*"]

GCOIN_BACKEND = 'gcoinbackend.backends.apibackend.GcoinAPIBackend'
GCOIN_BACKEND_SETTINGS = {
    'BASE_URL': OSS_API_URL,
    'KEY_STORE_CLASS': 'wallet.keystore.KeyStore'
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'evm_manager',
    'app',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oracle.urls'

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

WSGI_APPLICATION = 'oracle.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# loggin related settings
LOG_DIR = env('LOG_PATH', default=BASE_DIR + '/../../log/')
if len(LOG_DIR) == 0:
    LOG_DIR = LOG_DIR = BASE_DIR + '/../../log/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'state_log': {
            'format': "[%(asctime)s] %(threadName)s %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + 'django.log',
            'formatter': 'verbose'
        },
        'state_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'oracle_evm_manager.log'),
            'formatter': 'state_log',

        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'WARNING',
        },
        'django_crontab': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
        },
        'evm_manager': {
            'handlers': ['file', 'mail_admins', 'state_log_file'],
            'level': 'DEBUG',
        }
    }
}
