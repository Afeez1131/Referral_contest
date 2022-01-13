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
from .forms import GuestForm
from base_app.forms import GuestRegisterForm
from base_app.models import BusinessOwner, Referral, Guest
from .utils import get_ip_address
from django.contrib import messages


# Create your views here.


def ReferralHome(request, shortcode, ref_shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    referral = Referral.objects.get(
        business_owner=business, ref_shortcode=ref_shortcode
    )
    g_ip = get_ip_address(request)

    if request.method == "POST":
        form = GuestRegisterForm(request.POST)
        if form.is_valid():
            guest_instance = form.save(commit=False)
            guest_instance.referral = referral
            guest_instance.business = business
            guest_instance.ip = get_ip_address(request)

            try:
                guest = Guest.objects.get(business=business, referral=referral, ip=g_ip)

            except ObjectDoesNotExist:

                guest_instance = form.save(commit=False)
                guest_instance.referral = referral
                guest_instance.business = business
                guest_instance.ip = get_ip_address(request)
                guest_instance.save()
                return HttpResponseRedirect(guest_instance.guest_url)
            else:
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
        "Individual/homepage.html",
        {
            "referral": referral,
            "business": business,
            "form": form,
        },
    )


def ReferRedirect(request, shortcode, ref_shortcode):
    referral = Referral.objects.get(ref_shortcode=ref_shortcode)
    business = BusinessOwner.objects.get(shortcode=shortcode)
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


# crystaldesigns / VuVx
# def ReferRedirect(request, shortcode, ref_shortcode):
#     # b = BusinessOwner.objects.get(shortcode=shortcode)
#     # referral = Referral.objects.get(
#     #     ref_shortcode=ref_shortcode,
#     # business_owner=BusinessOwner.objects.get(shortcode=shortcode))
#
#     r = Referral.objects.get(ref_shortcode=ref_shortcode)
#     b = BusinessOwner.objects.get(shortcode=shortcode)
#     # print(type(request.META["REMOTE_ADDR"]))
#     try:
#         ip = get_ip_address(request)
#         print("IP Address :", ip)
#         qs = get_object_or_404(
#             Guest,
#             referral=r,
#             business=b,
#             ip=ip,
#             # get the ip address from the request, displays 127.0.0.1 locally
#             # guest_name=
#         )
#     except ObjectDoesNotExist:
#         qs = Guest(
#             referral=r,
#             business=b,
#             ip=ip,
#         )
#         qs.guest_count = qs.guest_count + 1
#         qs.save()
#         return HttpResponseRedirect(r.referral_url)
#
#     else:
#
#         return reverse("referral_home", args=(b.shortcode, r.ref_shortcode))


# def ReferRedirect(request, shortcode, ref_shortcode):
#     ref_shortcode = ref_shortcode
#     business = BusinessOwner.objects.get(shortcode=shortcode)
#     referral = Referral.objects.get(
#         ref_shortcode=ref_shortcode,
#         business_owner=business,
#     )
#
#     if request.method == "POST":
#         form = GuestForm(request.POST)
#
#         if form.is_valid():
#             guest_name = form.get("guest_name")
#             phone_number = form.get("phone_number")
#
#         try:
#             guest = Guest.objects.get(
#                 referral=referral,
#                 business=referral.business_owner,
#                 guest_name=guest_name,
#                 phone_number=phone_number,
#             )
#         except ObjectDoesNotExist:
#             guest = Guest(
#                 referral=referral,
#                 business=referral.business_owner,
#                 guest_name=guest_name,
#                 phone_number=phone_number,
#             )
#             guest.guest_count += 1
#             guest.save()
#             return HttpResponseRedirect(referral.referral_url)
#
#         else:
#             print("Guest : ", guest.guest_name, "exist before")
#             print("Shortcode :", business.shortcode)
#             print(BusinessOwner.objects.get(shortcode=business.shortcode))
#             return reverse("referral_home", args=(business.shortcode, ref_shortcode))
#     else:
#         form = GuestForm
#         return render(request, '')
#         # return reverse(
#         #     "referral_home",
#         #     shortcode=BusinessOwner.objects.get(shortcode=shortcode),
#         #     ref_shortcode=referral.ref_shortcode,
#         # )
