from django.urls import path
from . import views

urlpatterns = [
    path("<shortcode>/", views.ReferralHomeView, name="business_owner_profile"),
    path("<shortcode>/<contest_id>/", views.ContestDetail, name="contest_detail"),
    path(
        "<shortcode>/<contest_id>/referral/all/",
        views.ReferralList,
        name="referral_list",
    ),
    path(
        "register/<shortcode>/<contest_id>/",
        views.RegisterRefer,
        name="referral_register",
    ),
    path(
        "<shortcode>/<contest_id>/referral/<ref_shortcode>/",
        views.ReferralProfile,
        name="referral_profile",
    ),
    path(
        "export/<shortcode>/<contest_id>/",
        views.export_all_contact,
        name="export_all_contact",
    ),
]
