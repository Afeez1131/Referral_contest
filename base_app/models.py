from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from .utils import create_shortcode
from auth_app.models import Contest

# from auth_app.models import BusinessOwner
from django.conf import settings


class Referral(models.Model):
    business_owner = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name="referral_contest",
        null=True,
        blank=True,
    )
    refer_name = models.CharField(max_length=20)
    phoneNumberRegex = RegexValidator(
        regex=r"^0\d{10}$",
        message="Phone Number should be digits of 11 characters e.g. 08100550044",
    )
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)
    ref_shortcode = models.CharField(max_length=15, blank=True, unique=True)
    guest_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.ref_shortcode

    class Meta:
        ordering = ("-id",)
        unique_together = ("business_owner", "refer_name", "phone_number")

    def save(self, *args, **kwargs):
        if not self.guest_count:
            self.guest_count = self.guest_referral.count()
        # self.refer_message = str(self.refer_message) + " " + self.get_absolute_url()
        if not self.ref_shortcode:
            self.ref_shortcode = create_shortcode(self)
        super(Referral, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "referral_vote",
            kwargs={
                "shortcode": self.business_owner.business_owner.shortcode,
                "ref_shortcode": self.ref_shortcode,
                "contest_id": self.business_owner.id,
            },
        )


class Guest(models.Model):
    referral = models.ForeignKey(
        Referral, related_name="guest_referral", on_delete=models.CASCADE
    )
    business_owner = models.ForeignKey(
        Contest,
        related_name="contest_guest",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    ip = models.GenericIPAddressField(null=True)
    guest_name = models.CharField(max_length=100, null=True)
    phoneNumberRegex = RegexValidator(
        regex=r"^0\d{10}$",
        message="Phone Number should be digits of 11 characters e.g. 08100550044",
    )
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=11, null=True
    )

    def __str__(self):
        return str(self.guest_name)

    def save(self, *args, **kwargs):
        self.referral.guest_count += 1
        super(Guest, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-id",)
