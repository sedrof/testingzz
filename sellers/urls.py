from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "login/", Login.as_view(template_name="authenticate/login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "change_password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authenticate/change_password_done.html"
        ),
        name="password_change_done",
    ),
    path("password/", views.change_password, name="password_change"),
    path("create/", views.create_seller, name="create"),
    path("create/user/", views.create_user_api.as_view(), name="create_user"),
]
