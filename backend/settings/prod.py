from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")
TRUSTED_ADMIN_IP = "14.143.172.206"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("DATABASE_HOST"),
    "PORT": os.getenv("DATABASE_PORT"),
}

mongoengine.connect(
    db=os.getenv("MONGODB_NAME"),
    host=os.getenv("MONGODB_HOST"),
    port=os.getenv("MONGODB_PORT"),
)

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
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True  # Ensures the CSRF cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True  # Enforce the session cookie over HTTPS only
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"  # Prevent your site from being embedded in an iframe


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django_prod.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
            "suffix": "%Y-%m-%d",
        },
    },
}
