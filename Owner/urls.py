from django.urls import path
from . import views

urlpatterns = [
    path("<shortcode>/", views.ReferralHomeView, name="business_owner_profile"),
    path("referral/<shortcode>/all/", views.ReferralList, name="referral_list"),
    path("register/<shortcode>/", views.RegisterRefer, name="referral_register"),
    path(
        "referral/<shortcode>/<ref_shortcode>/",
        views.ReferralProfile,
        name="referral_profile",
    ),
]
