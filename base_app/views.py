from django.shortcuts import render
from auth_app.models import BusinessOwner
import urllib.parse
from django.template import RequestContext


# Create your views here.


def error_404(request, exception):
    data = {}
    return render(request, "base_app/404.html", data)


def error_500(request, exception):
    data = {}
    return render(request, "base_app/500.html", data)


def index(request):
    # business = BusinessOwner.objects.all()
    return render(request, "base_app/index.html", {})


def contact(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        message = request.POST.get("message")
        name = request.POST.get("name")
        full_message = (
            "Name: " + name + "\nMessage: " + message + "\nSender: " + phone_number
        )
        safe_string = urllib.parse.quote_plus(full_message)
        admin_no = "2348105506074"

        url_link = "https://wa.me/" + admin_no + "?text=" + safe_string
        print(url_link)
    return render(request, "base_app/contact.html", {})


def about(request):
    return render(request, "base_app/about.html", {})
