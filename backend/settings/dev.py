from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env.dev"
load_dotenv(dotenv_path=env_path)

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

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

# SESSION_ENGINE = "django.contrib.sessions.backends.db"

try:
    mongoengine.connect(
        host=os.getenv("MONGODB_CLUSTER"), db=os.getenv("MONGODB_DBNAME")
    )
    print("connected to local MongoDB!")
except Exception as e:
    print(e)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

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
