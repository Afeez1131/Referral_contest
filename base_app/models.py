from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from .utils import create_shortcode

# from auth_app.models import BusinessOwner
from django.conf import settings


class Referral(models.Model):
    business_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refer"
    )
    refer_name = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(
        regex=r"^0\d{10}$",
        message="Phone number must be entered in the format: '08105506070'. Up to 11 "
        "digits allowed.",
    )
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)
    ref_shortcode = models.CharField(
        max_length=10,
        blank=True,
        unique=True,
    )
    refer_message = models.CharField(
        max_length=100,
        default="Hello, i just signed up as a referral in your Referral Context, My name is ",
    )
    referral_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.ref_shortcode

    class Meta:
        ordering = ("-id",)
        unique_together = ("business_owner", "refer_name", "phone_number")

    def save(self, *args, **kwargs):
        self.refer_message = str(self.refer_message) + " " + str(self.refer_name)
        if not self.ref_shortcode:
            self.ref_shortcode = create_shortcode(self)
        else:
            self.ref_shortcode = self.ref_shortcode

        self.referral_url = (
            "https://wa.me/" + str(self.phone_number) + "?text=" + self.refer_message
        )
        super(Referral, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "referral_home",
            kwargs={
                "shortcode": self.business_owner.shortcode,
                "ref_shortcode": self.ref_shortcode,
            },
        )


class Guest(models.Model):
    referral = models.ForeignKey(
        Referral, related_name="guest_referral", on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guest_business",
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True)
    phoneNumberRegex = RegexValidator(
        regex=r"^0\d{10}$",
        message="Phone number must be entered in the format: '08105506070'. Up to 11 "
        "digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=11, null=True
    )
    guest_count = models.IntegerField(default=0)
    guest_url = models.CharField(max_length=200, blank=True)
    guest_message = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.guest_name

    def save(self, *args, **kwargs):
        self.guest_count += 1
        self.guest_message = (
            "Hello, I "
            + "was referred by "
            + str(self.referral)
            + " my name is "
            + str(self.guest_name)
        )
        self.guest_url = (
            "https://wa.me/"
            + str(self.business.phone_number)
            + "?text="
            + self.guest_message
        )

        super(Guest, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-id",)
