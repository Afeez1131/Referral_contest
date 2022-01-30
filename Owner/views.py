from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from auth_app.models import BusinessOwner
from base_app.models import Referral
from .forms import BusinessRegistrationForm, ReferralRegistration
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import re


@login_required(login_url="account_login")
def ReferralHomeView(request, shortcode):
    business = BusinessOwner.objects.filter(shortcode=shortcode)[0]
    # get the instance of the business owner using shortcode
    if request.user.username == business.username:
        # test if the login user is equal to the user Business Owner
        return render(
            request,
            "Owner/homepage.html",
            {
                "business": business,
            },
        )
    else:
        # messages.warning(request, "You do not have access to this page")
        return redirect("index")


def RegisterRefer(request, shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get a business owner with the shortcode passed as args
    referral = Referral.objects.filter(business_owner=business)
    # get the referral associated with the Business Owner

    if request.method == "POST":
        form = ReferralRegistration(request.POST)
        # the registration form
        if form.is_valid():
            refer_name = form.cleaned_data["refer_name"]
            phone_number = form.cleaned_data["phone_number"]
            # get the refer_name and phone number from the post request
            try:
                # try to get the referral with the provided details
                referral_instance = Referral.objects.get(
                    business_owner=business,
                    refer_name=refer_name,
                    phone_number=phone_number,
                )
            except Exception as ObjectDoesNotExist:
                # does not exist, create such referral
                referral_instance = Referral(
                    business_owner=business,
                    refer_name=refer_name,
                    phone_number=phone_number,
                )
                referral_instance.save()
                # save
                return redirect(
                    "referral_home", business.shortcode, referral_instance.ref_shortcode
                )
                # return HttpResponseRedirect(referral.referral_url)
            else:
                # if the referral exist, message notification
                messages.warning(
                    request,
                    "Referral "
                    + referral_instance.refer_name
                    + " exists, try again with a different Referral name",
                )
    else:
        form = ReferralRegistration()
    return render(
        request,
        "Owner/referral_list.html",
        {
            "form": form,
            "business": business,
            "referral": referral,
        },
    )


def ReferralProfile(request, shortcode, ref_shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    # get a busines Owner instance using the shortcode args
    referral = Referral.objects.get(ref_shortcode=ref_shortcode)
    # get the referral with the referral shortcode passed as args also

    return render(
        request,
        "Owner/referral_profile.html",
        {
            "business": business,
            "referral": referral,
        },
    )
