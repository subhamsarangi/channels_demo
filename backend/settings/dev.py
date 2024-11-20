from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = "not-very-secure-in-dev"

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE


DATABASES["default"] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("DATABASE_HOST"),
    "PORT": os.getenv("DATABASE_PORT"),
}

CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
