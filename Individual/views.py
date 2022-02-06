from django.http import Http404
from django.db.models import Q
from django.shortcuts import (
    render,
    HttpResponseRedirect,
    HttpResponse,
    get_object_or_404,
    redirect,
)
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from Individual.forms import GuestRegisterForm
from base_app.models import Referral, Guest
from auth_app.models import BusinessOwner
from .utils import get_ip_address
from django.contrib import messages
import urllib.parse

# Create your views here.


def VoteReferral(request, shortcode, ref_shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get the Business Owner instance using the Business Owner Shortcode args
    referral = Referral.objects.get(
        business_owner=business, ref_shortcode=ref_shortcode
    )
    # get the instance of the referral using the referral shortcode
    # and business Owner instance
    g_ip = get_ip_address(request)
    # get the IP of the current person

    if request.method == "POST":
        form = GuestRegisterForm(request.POST)
        # while trying to vote
        if form.is_valid():
            guest_name = request.POST["guest_name"]
            guest_instance = form.save(commit=False)
            guest_instance.referral = referral
            guest_instance.business = business
            guest_instance.ip = get_ip_address(request)

            try:
                guest = Guest.objects.get(business=business, referral=referral, ip=g_ip)
                # try getting a Guest with the business instance,
                # for the referral using the ref_shortcode, and for the current IP

            except ObjectDoesNotExist:
                # if it does not exist
                guest_instance = form.save(commit=False)
                guest_instance.referral = referral
                guest_instance.business = business
                guest_instance.ip = get_ip_address(request)
                # guest_instance.guest_count += 1
                # guest_instance.guest_count increment on save of guest in the model.
                guest_instance.save()
                # save the guest
                guest_message = (
                    r'Hello, I was referred by Referral ID: "5Hxh" my name is'
                    + guest_name
                )
                link = (
                    "https://wa.me/?text="
                    + urllib.parse.quote(guest_message)
                    # + urllib.parse.quote(vote_url)
                    # + urllib.parse.quote(signup_url)
                )
                return HttpResponseRedirect(guest_instance.guest_url)
            else:
                # if it exist, send a message notification
                messages.warning(
                    request,
                    "IP ["
                    + guest.ip
                    + "] voted for "
                    + referral.refer_name
                    + " Already. Multiple Votes not allowed",
                )
                return redirect(referral.get_absolute_url())

    else:
        form = GuestRegisterForm()

    return render(
        request,
        "Individual/guest_vote.html",
        {
            "referral": referral,
            "business": business,
            "form": form,
        },
    )


def ReferRedirect(request, shortcode, ref_shortcode):
    referral = Referral.objects.get(ref_shortcode=ref_shortcode)
    # get the referral instance using the referral shortcode
    business = BusinessOwner.objects.get(shortcode=shortcode)
    # get the business Owner using the shortcode args
    ip = get_ip_address(request)
    # will get the ip address of the current guest

    try:
        # guest = get_object_or_404(Guest, referral=referral, business=business)
        guest = Guest.objects.get(referral=referral, business=business)
        # check if we have a guest with referral and business passed from url arguments
        if ip == guest.ip:
            # check if the ip address of the current guest == ip address of a voted guest already
            return redirect(
                reverse(
                    "referral_home", args=(business.shortcode, referral.ref_shortcode)
                )
            )
        else:
            # if the ip of the current user is not an already voted guest for this referral, increment vote
            # count by 1
            guest.guest_count += 1
            guest.save()
            return HttpResponseRedirect(referral.referral_url)

    except ObjectDoesNotExist:
        # if guest does not exist before, create a new instance of guest
        guest = Guest(
            referral=referral,
            business=business,
            ip=ip,
        )
        guest.guest_count += 1
        # increment guest count by 1
        guest.save()
        return HttpResponseRedirect(guest.guest_url)
