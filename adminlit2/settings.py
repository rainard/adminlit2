"""
Django settings for adminlit2 project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from  . import base_config
setting_config = base_config.get_config()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'smxp$44jm%^3y_!qhy#9kbccfio-w7*!54xr^35!&v5v9^z#v9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
    'auth',
    'server',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adminlit2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR, 'templates' )],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminlit2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': setting_config.get('db_name'),
        'USER': setting_config.get('db_user'),
        'PASSWORD': setting_config.get('db_password'),
        'HOST': setting_config.get('db_host'),
        'PORT': setting_config.get('db_port'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8',
        }
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{0}:{1}/{2}".format(
            setting_config.get( 'redis_host' ),
            setting_config.get('redis_port'),
            setting_config.get( 'redis_db' )),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": setting_config.get('redis_passwd'),
            # socket 建立连接超时设置
            "SOCKET_CONNECT_TIMEOUT": 15,
            # 连接建立后的读写操作超时设置
            "SOCKET_TIMEOUT": 15,
            # 配置默认连接池
            "CONNECTION_POOL_KWARGS": {"max_connections": 20},
        }
    }
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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join( BASE_DIR, "static" ),
)

#========================================================


LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s  FilePath : %(pathname)s %(filename)s %(funcName)s %(lineno)d Message : %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(pathname)s %(filename)s %(funcName)s %(message)s'
        },
        'debug_for': {
            'format': '[%(asctime)s] \n\t Level     : %(levelname)s  \n\t FilePath  : %(pathname)s %(filename)s %(funcName)s %(lineno)d \n\t Message   : %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'formatter': 'debug_for',
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',  # message level to be written to console
        },
        'apscheduler.executors.default': {
            # logging handler that outputs log messages to terminal
            'formatter': 'debug_for',
            'class': 'logging.FileHandler',
            'filename': os.path.join( BASE_DIR, "logs/apscheduler.log" ),
        },
        'file_debug': {
            'level': 'DEBUG',
            'formatter': 'debug_for',
            'class': 'logging.FileHandler',
            'filename': os.path.join( BASE_DIR, "logs/debug.log" ),
        },
        'file_info': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join( BASE_DIR, "logs/info.log" ),
        },
        'file_error': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': os.path.join( BASE_DIR, "logs/error.log" ),
        },
        'file_mysql': {
            'level': 'DEBUG',
            'formatter': 'debug_for',
            'class': 'logging.FileHandler',
            'filename': os.path.join( BASE_DIR, "logs/mysql.log" ),
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['file_mysql'],
            'level': 'ERROR',
            'propagate': True,
        },
        'go.project': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apscheduler': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}












