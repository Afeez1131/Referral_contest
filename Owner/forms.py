from django import forms
from base_app.models import Referral, BusinessOwner
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.utils import IntegrityError


class BusinessRegistrationForm(forms.ModelForm):
    refer_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=11)

    class Meta:
        model = BusinessOwner
        # fields = "__all__"
        fields = ("business_name",)

    def clean(self):
        refer_name = self.cleaned_data["refer_name"]
        phone_number = self.cleaned_data["phone_number"]
        business_name = self.cleaned_data["business_name"]

        business = BusinessOwner.objects.get(business_name=business_name)
        print("Business :", business)
        qs = Referral.objects.filter(
            business_owner=business,
            refer_name=refer_name,
            phone_number=phone_number,
        )
        print("QS ", qs)
        if qs.exists():
            print("Qs exist: ")
            raise forms.ValidationError("ERROR: Ref " + refer_name + " already exists!")
        else:
            return self.cleaned_data
