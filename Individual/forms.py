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
        if str(phone_number).startswith("0"):
            phone_number_list = list(phone_number)
            phone_number_list[0] = "+234"
            p = "".join([str(elem) for elem in phone_number_list])
            print(p)
        return p
