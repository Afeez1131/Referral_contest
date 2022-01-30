from django.contrib.auth.forms import UserCreationForm
from auth_app.models import BusinessOwner
from base_app.models import Referral
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.forms import LoginForm
from django import forms
from django.core.validators import RegexValidator


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


#
# <input type="text" class="form-control" name="username" placeholder="08105505505" autocomplete="False">#}
# {#                                    <label for="floatingInput">Username or Phone Number</label>#}
# {#                                </div>#}
# {#                                <div class="mb-4 form-floating">#}
# {#                                    <input type="password" class="form-control" name="password" placeholder="Password">#}
# {#                                    <label for="floatingPassword">Password</label>#}


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = BusinessOwner
        fields = (
            "username",
            "phone_number",
            "full_name",
            "business_name",
            "reward_type",
            "password1",
            "password2",
        )
        # widgets = {
        #     "region": forms.ChoiceField(
        #         widget=forms.Select(attrs={"class": "dropdown-menu"})
        #     ),
        # }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # self.fields["username"] = forms.CharField(label='Phone Number', max_length=100)
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "Enter your username or phone number"
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["full_name"].widget.attrs["class"] = "form-control"

        self.fields["phone_number"].widget.attrs["class"] = "form-control"

        self.fields["business_name"].widget.attrs["class"] = "form-control"

        self.fields["password1"].widget = forms.PasswordInput()

        self.fields["password1"].widget.attrs["class"] = "form-control"

        self.fields["password2"].widget = forms.PasswordInput()

        self.fields["password2"].widget.attrs["class"] = "form-control"

        # self.fields["password2"].widget = forms.PasswordInput()
        # self.fields["password2"].widget.attrs[
        #     "placeholder"
        # ] = "Enter your username or phone number"
        self.fields["reward_type"].widget.attrs["class"] = "dropdown"
        self.fields[
            "reward_type"
        ].help_text = "Type of reward to give the winner of your contest"
