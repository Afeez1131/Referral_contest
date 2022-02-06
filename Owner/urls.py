from django.urls import path
from . import views

urlpatterns = [
    path("b/<shortcode>/", views.ReferralHomeView, name="business_owner_profile"),
    path("register/<shortcode>/", views.RegisterRefer, name="referral_register"),
    path("referral/<shortcode>/all/", views.ReferralList, name="referral_list"),
    path(
        "referral/<shortcode>/<ref_shortcode>/",
        views.ReferralProfile,
        name="referral_profile",
    ),
]
