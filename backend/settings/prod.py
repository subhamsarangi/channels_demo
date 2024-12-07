from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.getenv("DJANGO_ALLOWED_HOSTS")]

CSRF_TRUSTED_ORIGINS = [
    f'https://{os.getenv("DJANGO_ALLOWED_HOSTS")},
]

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")
dbname = os.getenv("MONGODB_DBNAME")

uri = f"mongodb+srv://{username}:{password}@{cluster}/{dbname}?retryWrites=true&w=majority"

try:
    mongoengine.connect(host=uri)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(uri, "\n", e)


# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }


# SECURE_SSL_REDIRECT = True
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


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#     },
#     "handlers": {
#         "file": {
#             "level": "ERROR",
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/django_prod.log"),
#             "when": "midnight",
#             "interval": 1,
#             "backupCount": 7,
#             "encoding": "utf-8",
#             "suffix": "%Y-%m-%d",
#         },
#     },
# }
