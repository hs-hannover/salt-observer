import os

# SECURITY WARNING:
# keep the secret key used in production secret!
# by the way, you should change it if you are reading this ;)
SECRET_KEY = 'l=fg3h+kynh^y77ac7k%4ubsk4wz=z&1ud8uy*m%p(iw8*+xp-'

# SECURITY WARNING:
# don't run with debug turned on in production!
DEBUG = True

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


# Session stuff
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 12 * 60 * 60  # 12H, because that's salts default token lifetime
SESSION_COOKIE_NAME = "cookie_session_salt_observer"

# Salt observer configuration
SALT_API = {
    'cherrypy': {
        'host': 'localhost',
        'port': 8001,
        'protocol': 'http',
    },
    'tornado': {
        'host': 'localhost',
        'port': 8002,
        'protocol': 'http'
    }
}

# specify your salt network here to disable it in network visualization
SALT_NETWORK = '123.456.789.0'
