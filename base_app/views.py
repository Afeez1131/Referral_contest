from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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
    admin_mail = settings.EMAIL_HOST_USER
    confirm_message = render_to_string('base_app/confirm_message.txt', {})
    if request.method == "POST":
        # phone_number = request.POST.get("phone")
        message = request.POST.get("message")
        name = request.POST.get("name")
        FROM = request.POST.get("email")

        try:
            send_mail(
                f'New Message from {name} on WhatsApp contest',
                message,
                FROM,
                [admin_mail],
                fail_silently=False,
            )
            send_mail(
                f'Hello, {name} We received your message on WhatsApp contest',
                confirm_message,
                admin_mail,
                [FROM],
                fail_silently=False,
            )
        except:
            messages.warning(request, 'We could not process your request right now, try again later.')

        messages.success(request, 'Message sent successfully.')
        return HttpResponseRedirect(reverse('contact'))
    return render(request, "base_app/contact.html", {})


def about(request):
    return render(request, "base_app/about.html", {})
