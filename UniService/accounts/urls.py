from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.logout_then_login, name="logout"),
]
