from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("DATABASE_HOST"),
    "PORT": os.getenv("DATABASE_PORT"),
}

CHANNEL_LAYERS["default"] = {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
        "hosts": [("127.0.0.1", 6379)],
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
