from django import forms
from base_app.models import Referral
from auth_app.models import BusinessOwner
from django.core.validators import RegexValidator


class BusinessRegistrationForm(forms.ModelForm):
    # refer_name = forms.CharField(max_length=50)
    # phoneNumberRegex = RegexValidator(
    #     regex=r"^0\d{10}$",
    #     message="Phone number must be entered in the format: '08105506070'. Up to 11 "
    #             "digits allowed.",
    # )
    # phone_number = forms.CharField(validators=[phoneNumberRegex], max_length=11)

    class Meta:
        model = Referral
        fields = ("refer_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(BusinessRegistrationForm, self).__init__(*args, **kwargs)

        self.fields["refer_name"].label = ""
        self.fields[
            "refer_name"
        ].help_text = "<small>Enter the name of the Referral</small>"
        self.fields["refer_name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Your name...",
        }

        self.fields["phone_number"].label = ""
        self.fields[
            "phone_number"
        ].help_text = "<small>Enter your WhatsApp Number...</small>"
        self.fields["phone_number"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Your Whatsapp No...",
        }


class ReferralRegistration(forms.ModelForm):
    # phoneNumberRegex = RegexValidator(
    #     regex=r"^0\d{10}$",
    #     message="Phone number must be entered in the format: '08105506070'. Up to 11 "
    #     "digits allowed.",
    # )
    # phone_number = forms.CharField(max_length=11)

    class Meta:
        model = Referral
        fields = ("refer_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(ReferralRegistration, self).__init__(*args, **kwargs)

        self.fields["refer_name"].label = ""
        self.fields["refer_name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Your name...",
        }

        self.fields["phone_number"].label = ""
        self.fields["phone_number"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Your Whatsapp No...",
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if str(phone_number).startswith("0"):
            phone_number_list = list(phone_number)
            phone_number_list[0] = "+234"
            p = "".join([str(elem) for elem in phone_number_list])
            print(p)
        return p
