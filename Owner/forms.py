from django import forms
from base_app.models import Referral
from auth_app.models import BusinessOwner, Contest
from django.core.validators import RegexValidator
from django.forms import ValidationError
from tempus_dominus.widgets import DateTimePicker


class BusinessRegistrationForm(forms.ModelForm):
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

    #
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        print(phone_number)
        return phone_number


class NewContestForm(forms.ModelForm):
    starting_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"],
        widget=DateTimePicker(
            attrs={
                "append": "fa fa-calendar",
                "icon_toggle": True,
            },
        ),
    )

    ending_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"],
        widget=DateTimePicker(
            attrs={
                "append": "fa fa-calendar",
                "icon_toggle": True,
            },
        ),
    )

    class Meta:
        model = Contest
        fields = ("cash_price", "starting_date", "ending_date")

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(NewContestForm, self).__init__(*args, **kwargs)

        # self.fields["username"] = forms.CharField(label='Phone Number', max_length=100)
        self.fields["cash_price"].widget.attrs[
            "placeholder"
        ] = "The total worth of the Cash/Product."
        self.fields["cash_price"].widget.attrs["class"] = "form-control"

        self.fields["starting_date"].widget.attrs["class"] = "form-control"
        # self.fields[
        #     "starting_date"
        # ].help_text = "Select starting date & time for your contest"

        self.fields["ending_date"].widget.attrs["class"] = "form-control"
        # self.fields[
        #     "ending_date"
        # ].help_text = "Select ending date & time for your contest"

    def clean_cash_price(self):
        cash_price = self.cleaned_data["cash_price"]
        print("Cash :", cash_price)
        if len(str(cash_price)) < 6:
            return cash_price
        else:
            raise ValidationError(
                "Ensure that there are no more than 5 digits in total."
            )
