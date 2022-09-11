from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserRegistrationForm, CustomLoginForm  # , ReferralRegistration
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from auth_app.models import BusinessOwner
from django.db.models import Q
from base_app.utils import slugify

# def home(request):
#     return render(request, "home.html", {})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("business_owner_profile", request.user.shortcode)
    else:
        if request.method == "POST":
            print(request.POST)
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration Successfull, Login Below")
                return redirect("account_login")

        else:
            form = UserRegistrationForm()

        return render(request, "account/signup.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("business_owner_profile", request.user.shortcode)
    else:
        if request.method == "POST":
            form = CustomLoginForm(request.POST)
            login_field = request.POST["login"]
            password = request.POST["password"]
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
                # authenticate the user
                if user is not None:
                    business = BusinessOwner.objects.get(
                        Q(username=login_field) | Q(phone_number=login_field)
                    )
                    login(request, user)
                    return redirect("business_owner_profile", business.shortcode)
        else:
            form = CustomLoginForm()
        return render(request, "account/login.html", {"form": form})


def logout_user(request):
    if request.user.is_authenticated and request.method == "POST":
        logout(request)
        return redirect("account_login")

    return render(request, "account/logout.html", {})


