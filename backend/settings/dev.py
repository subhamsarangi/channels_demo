from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
TRUSTED_ADMIN_IP = "192.168.1.190"

SECRET_KEY = "not-very-secure-in-dev"

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]


def show_toolbar(request):
    return True


SHOW_TOOLBAR_CALLBACK = show_toolbar

DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("DATABASE_HOST"),
    "PORT": os.getenv("DATABASE_PORT"),
}

mongoengine.connect(
    db="ninja_db",
    host="localhost",
    port=27017,
)

# SESSION_ENGINE = "django.contrib.sessions.backends.db"

CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django_dev.log"),
            "when": "D",  # Rotate logs daily
            "interval": 1,  # Rotate once per day
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
}
