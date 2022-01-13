from django.urls import path
from . import views

urlpatterns = [
    path("b/<shortcode>", views.BusinessOwnerView, name="owner_home"),
]
