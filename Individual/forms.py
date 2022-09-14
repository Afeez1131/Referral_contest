from django import forms
from django.core.validators import RegexValidator
from Individual.utils import get_ip_address
from django.forms import ValidationError
from base_app.models import Guest


class GuestRegisterForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ("guest_name", "phone_number")
        # widgets = {"ip": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(GuestRegisterForm, self).__init__(*args, **kwargs)
        self.fields["guest_name"].label = ""
        self.fields["guest_name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Your name",
        }

        self.fields["phone_number"].label = ""
        self.fields["phone_number"].widget.attrs = {
            "class": "form-control",
            "placeholder": "WhatsApp number...",
        }
