from django.urls import path
from . import views

urlpatterns = [
    path("profile/<shortcode>/", views.ReferralHomeView, name="business_owner_profile"),
    # path(
    #     "profile/<shortcode>/<ref_shortcode>/",
    #     views.ReferralProfile,
    #     name="referral_profile",
    # ),
    path("referral/<shortcode>/", views.RegisterRefer, name="referral_register"),
]
