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


def guest_vote_referral(request, shortcode, unique_id, ref_shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    contest = get_object_or_404(Contest, unique_id=unique_id, business_owner=business)
    referral = Referral.objects.get(business_owner=contest, ref_shortcode=ref_shortcode)

    ending_date = contest.ending_date
    starting_date = contest.starting_date

    if request.method == "POST":
        form = GuestRegisterForm(request.POST)
        # while trying to vote
        if form.is_valid():
            guest_name = form.cleaned_data["guest_name"]
            guest_phone = form.cleaned_data["phone_number"]
            guest_ip = get_ip_address(request)

            if contest.contest_time():
                guest_verify = Guest.objects.filter(
                    referral=referral,
                    business_owner=contest,
                    ip=guest_ip)

                guest_verify = Guest.objects.filter(referral=referral, business_owner=contest,phone_number=guest_phone)

                if not guest_verify.exists():
                    guest_instance = form.save(commit=False)
                    guest_instance.business_owner = contest
                    guest_instance.referral = referral
                    guest_instance.ip = guest_ip
                    guest_instance.referral.guest_count += 1

                    guest_instance.referral.save()
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
                        + urllib.parse.quote(guest_message))
                    return HttpResponseRedirect(whatsapp_link)

                else:
                    messages.warning(request, "Multiple vote from the same device/Number not allowed")

            elif timezone.now() < starting_date:
                messages.warning(
                    request,
                    "Voting has not started, starting by %s by %s"
                    % (
                        starting_date.strftime("%Y-%m-%d"),
                        starting_date.strftime("%H:%M:%S"),
                    ),
                )
            elif contest.past_contest_time():
                messages.warning(
                    request,
                    "You can no longer join this contest as it ended on %s by %s"
                    % (
                        ending_date.strftime("%Y-%m-%d"),
                        ending_date.strftime("%H:%M:%S"),
                    ),
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
            'contest': contest
        },
    )
