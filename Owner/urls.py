from django.urls import path
from . import views

urlpatterns = [
    path("<shortcode>/", views.business_owner_home, name="business_owner_profile"),
    path("contest/<unique_id>/", views.contest_detail, name="contest_detail"),
    path(
        "<shortcode>/contest/<unique_id>/referral/all/",
        views.referral_list,
        name="referral_list",
    ),
    path("register/<shortcode>/<unique_id>/", views.register_referral, name="referral_register",
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
