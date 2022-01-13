from django import forms


class GuestForm(forms.Form):
    guest_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=11)
