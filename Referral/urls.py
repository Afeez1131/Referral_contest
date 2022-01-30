"""Referral URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from auth_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base_app.urls")),
    path("", include("Owner.urls")),
    path("", include("Individual.urls")),
    path("", include("Analytic.urls")),
    path("", include("auth_app.urls")),
    path("accounts/", include("allauth.urls")),
    # path("accounts/referral/login/", views.login_referral, name="referral_login"),
    # path("accounts/referral/signup/", views.register_referral, name="referral_signup"),
]
