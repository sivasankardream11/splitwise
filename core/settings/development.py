# Development Settings
from .base import *

# Debug mode enabled
DEBUG = True

# Added localhost to allowed hosts
ALLOWED_HOSTS += ['*', ]

# CORS settings: Allowed origins
CORS_ALLOWED_ORIGINS = [
    "https://split_wise.techasoft.com",
    "http://localhost:5173",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Content-Disposition',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Add maintenance_mode app to installed apps
INSTALLED_APPS += [
    'maintenance_mode',
]

# Add maintenance_mode middleware
MIDDLEWARE += [
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': os.environ.get('DB_CNF_PATH'),
#         },
#     }
# }

# Use SQLite3 for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file location
    }
}
# Static files settings
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# Maintenance mode settings
MAINTENANCE_MODE = False
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True

# Update JWT settings for token lifetimes and sliding tokens
SIMPLE_JWT.update({
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
})

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'LOCATION': MEDIA_ROOT,  # Specify the directory where files will be stored
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
