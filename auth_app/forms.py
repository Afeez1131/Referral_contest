from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django import forms


# class CustomUserCreationForm(SignupForm):
#     business_name = forms.CharField(max_length=100)
#
#     class Meta:
#         model = get_user_model()
#         fields = ("email", "username", "business_name")


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = (
#             "email",
#             "username",
#         )
