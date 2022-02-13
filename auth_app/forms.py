from django.contrib.auth.forms import UserCreationForm
from auth_app.models import BusinessOwner
from allauth.account.forms import LoginForm
from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # self.fields["username"] = forms.CharField(label='Phone Number', max_length=100)
        self.fields["login"].label = "Username or Phone Number"
        self.fields["login"].widget.attrs[
            "placeholder"
        ] = "Enter your username or phone number"
        self.fields["login"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget = forms.PasswordInput()
        self.fields["password"].widget.attrs[
            "placeholder"
        ] = "Enter your username or phone number"
        self.fields["password"].widget.attrs["class"] = "form-control"

        # You don't want the `remember` field?
        if "remember" in self.fields.keys():
            del self.fields["remember"]


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = BusinessOwner
        fields = (
            "username",
            "phone_number",
            "full_name",
            "business_name",
            "cash_price",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # self.fields["username"] = forms.CharField(label='Phone Number', max_length=100)
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "Enter your username or phone number"
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["full_name"].widget.attrs["class"] = "form-control"
        self.fields["full_name"].widget.attrs["placeholder"] = "your Full name..."

        self.fields["phone_number"].widget.attrs["class"] = "form-control"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number..."
        self.fields["phone_number"].help_text = "Enter your 11 digit phone number"

        self.fields["business_name"].widget.attrs["class"] = "form-control"
        self.fields["business_name"].widget.attrs["placeholder"] = "Business Name..."

        self.fields["password1"].widget = forms.PasswordInput()
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password..."

        self.fields["password2"].widget = forms.PasswordInput()
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password..."

        self.fields["cash_price"].widget.attrs[
            "placeholder"
        ] = "Enter the amount to spend on the contest"
        self.fields["cash_price"].widget.attrs["class"] = "form-control"

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if str(phone_number).startswith("0") and len(str(phone_number)) == 11:
            phone_number_list = list(phone_number)
            phone_number_list[0] = "234"
            p = "".join([str(elem) for elem in phone_number_list])
            return p

        else:
            raise ValidationError(
                _(
                    "Incorrect Phone Number entered check the phone number and try again. e.g 08035221111"
                )
            )
