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
from auth_app.models import BusinessOwner, Contest
from .utils import get_ip_address, phone_num_val
from django.contrib import messages
import urllib.parse
from django.db.models import Q

# Create your views here.

from django.utils import timezone


def VoteReferral(request, shortcode, contest_id, ref_shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get the Business Owner instance using the Business Owner Shortcode args
    contest = get_object_or_404(Contest, id=contest_id, business_owner=business)
    # get the contest using the id, and business_owner
    referral = Referral.objects.get(business_owner=contest, ref_shortcode=ref_shortcode)
    # get the instance of the referral using the referral shortcode
    # and business Owner instance

    ending_date = contest.ending_date
    starting_date = contest.starting_date
    # the date and time to end the contest

    if request.method == "POST":
        form = GuestRegisterForm(request.POST)
        # while trying to vote
        if form.is_valid():  # check if the form is valid
            guest_name = form.cleaned_data["guest_name"]  # get the guest_name
            guest_phone = form.cleaned_data["phone_number"]  # get the phone_number
            guest_ip = get_ip_address(request)

            try:  # try and see if the same guest with all above fields exist
                guest = Guest.objects.get(
                    ip=guest_ip,
                    guest_name=guest_name,
                    phone_number=guest_phone,
                    business_owner=contest,
                    referral=referral,
                )

            except Exception as ObjectDoesNotExist:
                guest_instance = form.save(commit=False)
                guest_instance.business_owner = contest
                guest_instance.referral = referral
                guest_instance.ip = guest_ip
                # if the object does not exist

                if (starting_date < timezone.now()) and (ending_date > timezone.now()):
                    try:
                        guest_verify = Guest.objects.get(
                            referral=guest_instance.referral,
                            business_owner=contest,
                            ip=guest_instance.ip,
                        )
                    except Exception as ObjectDoesNotExist:
                        guest_instance.save()
                        guest_message = (
                            r"Hello, I was referred by Referral "
                            + referral.refer_name
                            + " my name is "
                            + guest_name
                        )
                        whatsapp_link = (
                            "https://wa.me/"
                            + str(phone_num_val(business.phone_number))
                            + "?text="
                            + urllib.parse.quote(guest_message)
                            # + urllib.parse.quote(vote_url)
                            # + urllib.parse.quote(signup_url)
                        )
                        return HttpResponseRedirect(whatsapp_link)
                    else:
                        messages.warning(
                            request, "Multiple vote from the same device not allowed"
                        )
                elif timezone.now() < starting_date:
                    """if the time for ending vote has not reached"""
                    messages.warning(
                        request,
                        "Voting has not started, starting by %s by %s"
                        % (
                            starting_date.strftime("%Y-%m-%d"),
                            starting_date.strftime("%H:%M:%S"),
                        ),
                    )
                else:
                    """if the time for ending vote has reached/passed"""
                    messages.warning(
                        request,
                        "You can no longer join this contest has it ended on %s by %s"
                        % (
                            ending_date.strftime("%Y-%m-%d"),
                            ending_date.strftime("%H:%M:%S"),
                        ),
                    )

            else:  # if it exist, Then there is exactly the above guest in the db
                # print("Guest exists")
                messages.warning(
                    request,
                    "Guest %s voted already" % guest.guest_name,
                )

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


""" gname = guest3
ref_shortcode=9r2d
phone_number= 08105506601
"""

'''                    if guest.filter(
                        Q(guest_name=guest.guest_name)
                        | Q(ip=guest.ip)
                        | Q(phone_number=guest.phone_number)
                    ).exists():
                        """check to see if there is a referral and business owner with the same
                        phone number or ip address or guest name with the one we just want to save"""
                        messages.warning(
                            request,
                            "Multiple vote not allowed",
                        )
                        # print("Either name, phone number or ip exists")
                    else:'''
