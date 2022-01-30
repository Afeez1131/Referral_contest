from django import forms
from django.core.validators import RegexValidator


from base_app.models import Guest


class GuestRegisterForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ("guest_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(GuestRegisterForm, self).__init__(*args, **kwargs)
        self.fields["guest_name"].label = ""
        self.fields["guest_name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter guest name...",
        }

        self.fields["phone_number"].label = ""
        self.fields["phone_number"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter phone number...",
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        phoneNumberRegex = RegexValidator(
            regex=r"^0\d{10}$",
            message="Phone number must be entered in the format: '08105506070'. Up to 11 "
            "digits allowed.",
        )
        phoneNumberRegex(phone_number)
        return phone_number
