from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserRegistrationForm, CustomLoginForm  # , ReferralRegistration
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from auth_app.models import BusinessOwner
from django.db.models import Q


# def home(request):
#     return render(request, "home.html", {})


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successfull, Login Below")
            return redirect("account_login")
        # after registration, redirect to the login page
        # else:
        #     print("Invalid FOrm :", form)
        #     messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserRegistrationForm()

    return render(request, "account/signup.html", {"form": form})


# def register_referral(request):
#     if request.method == "POST":
#         form = ReferralRegistration(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("account_login")
#         # else:
#         #     print("Invalid FOrm :", form)
#         #     messages.error(request, "Unsuccessful registration. Invalid information.")
#     else:
#         form = ReferralRegistration()
#
#     return render(request, "account/signup.html", {"form": form})


# def login_referral(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("home")
#         messages.warning(request, "Incorrect login details provided")
#
#     return render(request, "account/login.html", {})


def login_user(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)  # login form
        login_field = request.POST["login"]
        password = request.POST["password"]
        # since it is a login form, and we are not saving to the DB
        # got the username and password using request.POST and the name of the field
        user = authenticate(request, username=login_field, password=password)
        # authenticate the user
        if user is not None:
            # if the user exist
            # business = BusinessOwner.objects.get(username=login_field)
            business = BusinessOwner.objects.get(
                Q(username=login_field) | Q(phone_number=login_field)
            )
            # get a business owner with the
            # next = business.get_absolute_url()
            login(request, user)
            return redirect("business_owner_profile", business.shortcode)
        else:
            messages.warning(request, "Incorrect login details provided")
    form = CustomLoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_user(request):
    if request.user.is_authenticated and request.method == "POST":
        # check to see if the user that want to logout is authenticated
        # also check if the request is a Post request, then logout the
        # currently authenticated user
        logout(request)
        return redirect("account_login")
    # redirect to the login page
    else:
        return render(request, "account/logout.html", {})
