from django.urls import path
from . import views

urlpatterns = [
    path(
        "vote/<shortcode>/<contest_id>/<ref_shortcode>/",
        views.VoteReferral,
        name="referral_vote",
    ),
    # path(
    #     "ref/<shortcode>/<ref_shortcode>/",
    #     views.ReferRedirect,
    #     name="referral_redirect",
    # ),
]
