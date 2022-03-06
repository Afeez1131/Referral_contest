from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.urls import reverse
from django.contrib import messages
from auth_app.models import BusinessOwner, Contest
from base_app.models import Referral, Guest
from .forms import BusinessRegistrationForm, ReferralRegistration, NewContestForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import re
from base_app.utils import create_shortcode
import urllib.parse
from .utils import make_vcard, write_vcard


# @login_required(login_url="account_login")
# def ReferralHomeView(request, shortcode):
#     business = BusinessOwner.objects.get(shortcode=shortcode)
#     print("business", business)
#     # get the instance of the business owner using shortcode
#
#     if request.user.username == business.username:
#         # test if the login user is equal to the user Business Owner
#         share_message = (
#             "Stand a chance of winning a cash/product of #"
#             + str(business.cash_price)
#             + " by "
#             "referring people to " + business.business_name + ".\n Get started here: "
#         )
#
#         signup_url = request.build_absolute_uri(
#             reverse("referral_register", args=(business.shortcode,))
#         )
#
#         if request.method == "POST":
#             link = "https://wa.me/?text=" + urllib.parse.quote(
#                 share_message + signup_url
#             )
#             print("Link: ", link)
#             return HttpResponseRedirect(link)
#         return render(
#             request,
#             "Owner/referral_homepage.html",
#             {
#                 "business": business,
#                 "share_message": share_message,
#                 "signup_url": signup_url,
#             },
#         )
#     else:
#         # messages.warning(request, "You do not have access to this page")
#         return redirect("index")


@login_required(login_url="account_login")
def ReferralHomeView(request, shortcode):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get the business or 404 using shortcode
    contests = Contest.objects.filter(business_owner=business)
    if request.method == "POST":
        form = NewContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.business_owner = business
            contest.save()
            # form.save()
            return redirect("contest_detail", business.shortcode, contest.id)

    else:
        form = NewContestForm()
    return render(
        request,
        "Owner/referral_homepage.html",
        {
            "business": business,
            "form": form,
            "contests": contests,
            # "share_message": share_message,
            # "signup_url": signup_url,
        },
    )


@login_required(login_url="account_login")
def ContestDetail(request, shortcode, contest_id):
    # get the instance of the business owner using shortcode
    business = BusinessOwner.objects.get(shortcode=shortcode)
    contest = get_object_or_404(Contest, business_owner=business, id=contest_id)
    share_message = (
        "Stand a chance of winning a cash/product of #"
        + str(contest.cash_price)
        + " by "
        "referring people to " + business.business_name + ".\n Get started here: "
    )

    signup_url = request.build_absolute_uri(
        reverse("referral_register", args=(business.shortcode, contest.id))
    )

    if request.method == "POST":
        link = "https://wa.me/?text=" + urllib.parse.quote(share_message + signup_url)
        return HttpResponseRedirect(link)
    return render(
        request,
        "Owner/contest_detail.html",
        {
            "business": business,
            "contest": contest,
            "share_message": share_message,
            "signup_url": signup_url,
        },
    )


@login_required(login_url="account_login")
def ReferralList(request, shortcode, contest_id):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    contest = get_object_or_404(Contest, id=contest_id, business_owner=business)
    # get a business owner with the shortcode passed as args
    # obj_list = get_list_or_404(Referral, business_owner=business)
    ref_dict = {}
    referral = Referral.objects.filter(business_owner=contest).order_by("-guest_count")
    ref_list = Referral.objects.values_list("guest_count", flat=True)
    print(ref_list, referral)

    # referral = obj_list[0]
    # get the referral associated with the Business Owner
    return render(
        request,
        "Owner/referral_list.html",
        {
            "referral": referral,
            "business": business,
            "contest": contest,
        },
    )


from django.utils import timezone


# @login_required(login_url="account_login")
def RegisterRefer(request, shortcode, contest_id):
    business = get_object_or_404(BusinessOwner, shortcode=shortcode)
    # get a business owner with the shortcode passed as args
    # obj_list = get_list_or_404(Referral, business_owner=business)
    contest = get_object_or_404(Contest, id=contest_id, business_owner=business)
    referral = Referral.objects.filter(business_owner=contest)
    ending_date = contest.ending_date
    # referral = obj_list[0]
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
                # referral = Referral.objects.filter(business_owner=business)
                referral_instance = Referral.objects.get(
                    business_owner=contest,
                    refer_name=refer_name,
                    phone_number=phone_number,
                )
            except Exception as ObjectDoesNotExist:
                if timezone.now() < ending_date:
                    # if object does not exist, check if the ending date is
                    # not yet reached
                    # does not exist, create such referral
                    # referral = Referral.objects.filter(business_owner=business)
                    referral_instance = Referral(
                        business_owner=contest,
                        refer_name=refer_name,
                        phone_number=phone_number,
                    )
                    shortcode = create_shortcode(referral_instance, size=4)
                    referral_instance.ref_shortcode = shortcode
                    referral_instance.save()
                    # save
                    return redirect(
                        "referral_profile",
                        contest.business_owner.shortcode,
                        contest.id,
                        referral_instance.ref_shortcode,
                    )
                else:

                    # if the current time == the ending time
                    messages.warning(
                        request,
                        "You can no longer join this contest has it ended on %s"
                        % ending_date,
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
        "Owner/referral_register.html",
        {
            "form": form,
            "business": business,
            "referral": referral,
        },
    )


def ReferralProfile(request, shortcode, contest_id, ref_shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    # get a busines Owner instance using the shortcode args
    contest = get_object_or_404(Contest, id=contest_id, business_owner=business)
    # get the contest using the contest id, and business owner
    referral = Referral.objects.get(ref_shortcode=ref_shortcode, business_owner=contest)
    # get the referral with the referral shortcode passed as args also

    vote_url = request.build_absolute_uri(
        reverse(
            "referral_vote",
            args=(business.shortcode, contest.id, referral.ref_shortcode),
        )
    )
    referral_message = (
        "Hello, i am participating in a referral contest, the person with the highest "
        "vote wins the Cash/Gift price. kindly vote for me here:\n"
    )
    if request.method == "POST":
        referral_link = "https://wa.me/?text=" + urllib.parse.quote(
            referral_message + vote_url
        )
        # will encode the text and url to avoid errors

        # will handle the sharing of the message on whatsapp
        return HttpResponseRedirect(referral_link)

    return render(
        request,
        "Owner/referral_profile.html",
        {
            "business": business,
            "referral": referral,
            "vote_url": vote_url,
            "referral_message": referral_message,
        },
    )


def export_all_contact(request, shortcode, contest_id):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    contest = get_object_or_404(Contest, id=contest_id, business_owner=business)
    referral = Referral.objects.filter(business_owner=contest)
    guest = Guest.objects.filter(business_owner=contest)

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
        vcard = make_vcard(name + "-" + str(business.shortcode), number)
        # convert the k, v into vcard object
        vcard_list.append(vcard)
    # append the vcard obj to a list

    for line in vcard_list:
        # get the first list
        response.writelines([l + "\n" for l in line])

    return response
