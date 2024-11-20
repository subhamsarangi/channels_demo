from django.contrib import admin
from django.urls import path, include
from django.conf import settings

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
    from django.conf.urls.static import static
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
