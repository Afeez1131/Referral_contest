from django.urls import path
from . import views

urlpatterns = [
    path(
        "profile/<shortcode>/<ref_shortcode>/", views.VoteReferral, name="referral_home"
    ),
    path(
        "ref/<shortcode>/<ref_shortcode>/",
        views.ReferRedirect,
        name="referral_redirect",
    ),
]
