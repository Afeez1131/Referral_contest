from django import forms
from base_app.models import Guest


class GuestRegisterForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ("guest_name", "phone_number")
