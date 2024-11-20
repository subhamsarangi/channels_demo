from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.api.views import api_api
from apps.chat.views import chat_api
from apps.tasks.views import tasks_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.myauth.urls")),
    path("api/", api_api.urls),
    path("chat/", chat_api.urls),
    path("", tasks_api.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
