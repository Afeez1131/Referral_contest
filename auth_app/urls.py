from django.urls import path
from . import views


urlpatterns = [
    # path("", views.home, name="home"),
    path("accounts/login/", views.login_user, name="account_login"),
    path("accounts/logout/", views.logout_user, name="account_logout"),
    path("accounts/signup/", views.register_view, name="account_signup"),
]
