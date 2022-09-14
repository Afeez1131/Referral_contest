from django.contrib.auth.forms import UserCreationForm
from auth_app.models import BusinessOwner
from base_app.models import Contest
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
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-mask', 'autocomplete': "off", 'data-mask': "0000-000-0000", 'placeholder': "Phone Number (080x-xxx-xxxx)"}))

    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Full Name", 'autocomplete': "off"}))

    class Meta:
        model = BusinessOwner
        fields = (
            "username",
            "phone_number",
            "full_name",
            "business_name",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        return phone.replace('-', '')

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        print("name", name)
        name_list = name.split(' ')
        if len(name_list) < 2:
            raise forms.ValidationError('Ensure to enter your first and last name.')
        return name.title()

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # self.fields["username"] = forms.CharField(label='Phone Number', max_length=100)
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "username/phone number"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].help_text = " "


        self.fields["business_name"].widget.attrs["class"] = "form-control"
        self.fields["business_name"].widget.attrs["placeholder"] = "Business Name..."
        self.fields["business_name"].help_text = " "

        self.fields["password1"].widget = forms.PasswordInput()
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password..."
        self.fields["password1"].help_text = " "

        self.fields["password2"].widget = forms.PasswordInput()
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password..."
        self.fields["password2"].help_text = ""


