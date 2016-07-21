import os

# SECURITY WARNING:
# keep the secret key used in production secret!
# by the way, you should change it if you are reading this ;)
SECRET_KEY = 'l=fg3h+kynh^y77ac7k%4ubsk4wz=z&1ud8uy*m%p(iw8*+xp-'

# SECURITY WARNING:
# don't run with debug turned on in production!
DEBUG = False

# change this!
ALLOWED_HOSTS = ['localhost']


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
    }
}
