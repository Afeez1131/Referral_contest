from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from base_app.models import BusinessOwner, Referral
from .forms import BusinessRegistrationForm

# Create your views here.


def BusinessOwnerView(request, shortcode):
    business = BusinessOwner.objects.get(shortcode=shortcode)
    # get the instance of the business owner using shortcode

    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST, instance=business)
        # use the business model to create a form in forms.py,
        # with an instance of the business

        if form.is_valid():
            data = form.cleaned_data
            refer_name = data["refer_name"]
            phone_number = data["phone_number"]

            referral = Referral(
                business_owner=business,
                refer_name=refer_name,
                phone_number=phone_number,
            )
            referral.save()
            return HttpResponseRedirect(referral.referral_url)

    else:
        form = BusinessRegistrationForm(instance=business)

    return render(
        request,
        "Owner/homepage.html",
        {
            "business": business,
            "form": form,
        },
    )
