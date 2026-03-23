from .base import *

DEBUG = True
SECRET_KEY = 'test-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']

# Use SQLite for tests — no Postgres/Redis needed in CI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable Redis cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
