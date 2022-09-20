import json

from django.http import HttpResponseRedirect
from django.shortcuts import (render, HttpResponse, redirect, get_object_or_404, get_list_or_404, )
from django.urls import reverse
from django.contrib import messages

from Individual.forms import GuestRegisterForm
from auth_app.models import BusinessOwner, Contest
from base_app.models import Referral, Guest
from .forms import BusinessRegistrationForm, ReferralRegistration, NewContestForm
from django.contrib.auth.decorators import login_required
import re
from base_app.utils import create_shortcode
import urllib.parse
from django.utils import timezone
from .utils import make_vcard, write_vcard


@login_required(login_url="account_login")
def business_owner_home(request):
    shortcode = request.user.shortcode
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    contests = Contest.objects.filter(business_owner=business)
    form = NewContestForm()

    if request.method == "POST":
        form = NewContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.business_owner = business
            contest.save()
            return HttpResponseRedirect(reverse("contest_detail", args=[contest.unique_id]))

    return render(request, "Owner/referral_homepage.html",
        {"business": business, "form": form, "contests": contests, }, )


@login_required
def business_new_contest(request):
    form = NewContestForm()
    shortcode = request.user.shortcode
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # contests = Contest.objects.filter(business_owner=business)

    if request.method == 'POST':
        form = NewContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.business_owner = business
            contest.save()
            # form.save()
            messages.success(request, 'Contest created successfully.')
            return HttpResponseRedirect(reverse("contest_detail", args=[contest.unique_id]))
    return render(request, 'Owner/new_contest.html', {'form': form, 'business': business})


@login_required
def business_all_contest(request):
    user_shortcode = request.user.shortcode
    business = get_object_or_404(BusinessOwner, shortcode=user_shortcode)
    contests = business.contests.all()
    print(contests)

    return render(request, 'Owner/all_contest.html', {'contests': contests, 'business': business})


@login_required(login_url="account_login")
def contest_detail(request, unique_id):
    business = BusinessOwner.objects.get(shortcode=request.user.shortcode)
    contest = get_object_or_404(Contest, business_owner=business, unique_id=unique_id)
    signup_url = request.build_absolute_uri(reverse("referral_register", args=(business.shortcode, contest.unique_id)))
    share_message = f"Stand a chance of winning a cash/product price of # {contest.cash_price}" \
                    f" just by referring people to {business.business_name}. Get started here: {signup_url}"

    if request.method == "POST":
        link = "https://wa.me/?text=" + urllib.parse.quote(share_message)
        return HttpResponseRedirect(link)
    return render(request, "Owner/contest_detail.html",
        {"business": business, "contest": contest, "share_message": share_message, "signup_url": signup_url, }, )


# @login_required(login_url="account_login")
def referral_list(request, shortcode, unique_id):
    form = GuestRegisterForm()
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    contest = get_object_or_404(Contest, unique_id=unique_id, business_owner=business)
    # referral = Referral.objects.filter(contest=contest)
    referral = contest.referral_set.all().order_by('-guest_count')
    # ref_list = Referral.objects.values_list("refer_name", "ref_shortcode", "guest_referral")

    return render(request, "Owner/referral_list.html",
        {"referral": referral, "business": business, "contest": contest, "form": form, }, )


def register_referral(request, shortcode, unique_id):
    form = ReferralRegistration()

    business = get_object_or_404(BusinessOwner, shortcode=shortcode)

    contest = get_object_or_404(Contest, unique_id=unique_id, business_owner=business)
    referral = Referral.objects.filter(contest=contest)
    ending_date = contest.ending_date
    starting_date = contest.starting_date

    if request.method == "POST":
        print(request.POST)
        form = ReferralRegistration(request.POST)
        if form.is_valid():
            refer_name = form.cleaned_data["refer_name"]
            phone_number = form.cleaned_data["phone_number"]

            if contest.contest_time:
                referral_instance = Referral.objects.filter(contest=contest)
                referral_instance = referral_instance.filter(phone_number=phone_number)

                if not referral_instance.exists():
                    referral_instance = Referral(contest=contest, refer_name=refer_name,
                                                 phone_number=phone_number)

                    shortcode = create_shortcode(referral_instance, size=4)
                    referral_instance.ref_shortcode = shortcode
                    referral_instance.contest.referral_count += 1

                    referral_instance.contest.save()
                    referral_instance.save()
                    print(referral_instance, shortcode)
                    # save
                    return HttpResponseRedirect(reverse("referral_profile",
                                                        args=[contest.business_owner.shortcode, contest.unique_id,
                                                              referral_instance.ref_shortcode]))
                else:
                    messages.warning(request, 'A Referral exist with this Phone Number, try again.')

            elif timezone.now() < starting_date:
                print('not time yet')
                time_left = '{:.2f}'.format(((starting_date - timezone.now()).total_seconds()) / 60)
                messages.warning(request, f'The contest has not started'
                                          f' you can only register as a referral once the contest begins. Kindly , checkback in '
                                          f' {time_left} Minutes. ')

            elif contest.past_contest_time:
                print('contest ended')
                # if the current time == the ending time
                messages.warning(request, "You can no longer join this contest has it ended on %s" % ending_date, )

    return render(request, "Owner/referral_register.html",
        {"form": form, "business": business, "referral": referral, }, )


def referral_profile(request, shortcode, unique_id, ref_shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    contest = get_object_or_404(Contest, unique_id=unique_id, business_owner=business)
    referral = Referral.objects.get(ref_shortcode=ref_shortcode, contest=contest)

    vote_url = request.build_absolute_uri(
        reverse("referral_vote", args=[business.shortcode, contest.unique_id, referral.ref_shortcode], ))
    referral_message = ("Hello, i am participating in a referral contest, the person with the highest "
                        f"vote wins the Cash/Gift price. kindly vote for me here: {vote_url}")

    if request.method == "POST":
        referral_link = "https://wa.me/?text=" + urllib.parse.quote(referral_message + vote_url)

        return HttpResponseRedirect(referral_link)

    return render(request, "Owner/referral_profile.html",
        {"business": business, "referral": referral, "vote_url": vote_url, "referral_message": referral_message, }, )


def export_all_contact(request, shortcode, unique_id):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    contest = get_object_or_404(Contest, unique_id=unique_id, business_owner=business)
    referral = Referral.objects.filter(contest=contest)
    guest = Guest.objects.filter(contest=contest)

    file_name = str(business.shortcode) + "-contact.vcf"
    response = HttpResponse(content_type="text/x-vCard")
    response["Content-Disposition"] = 'attachment; filename="%s"' % file_name

    name_phone = dict()  # the dictionary for the name and phone number
    vcard_list = list()  # the vcard obj dict.
    c = 0

    for ref in referral:
        if ref.refer_name not in name_phone.keys():
            name_phone[ref.refer_name] = ref.phone_number
        else:
            c += 1
            ref.refer_name = ref.refer_name + "-" + str(c)
            name_phone[ref.refer_name] = ref.phone_number

    for g in guest:
        if g.guest_name not in name_phone.keys():
            name_phone[g.guest_name] = g.phone_number
        else:
            c += 1
            g.guest_name = g.guest_name + "-" + str(c)
            name_phone[g.guest_name] = g.phone_number

    for name, number in name_phone.items():
        vcard = make_vcard(name, number)
        # convert the k, v into vcard object
        vcard_list.append(vcard)
    # append the vcard obj to a list

    for line in vcard_list:
        # get the first list
        response.writelines([l + "\n" for l in line])

    return response
