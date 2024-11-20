from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView

app_name = "myauth"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
