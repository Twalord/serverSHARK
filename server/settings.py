from .base import *

#
#  SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6-og!lz7^&+f$cj#-0!68^rxm!#8$t=o&ypw)6d6a2t5_ntc1@'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartshark',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost'
    },
    'mongodb' : {
        'ENGINE': '',
        'NAME': 'smartshark',
        'USER': 'root',
        'PASSWORD': 'balla1234$',
        'HOST': 'localhost',
        'PORT': 27017,
        'AUTHENTICATION_DB': 'admin'
    }
}