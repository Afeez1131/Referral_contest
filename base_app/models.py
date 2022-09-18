from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from .utils import create_shortcode
from auth_app.models import Contest
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Referral(models.Model):
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
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
    guest_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.ref_shortcode

    class Meta:
        ordering = ("-id",)
        unique_together = ("contest", "refer_name", "phone_number")

    def save(self, *args, **kwargs):

        if not self.ref_shortcode:
            self.ref_shortcode = create_shortcode(self)
        super(Referral, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "referral_vote",
            kwargs={
                "shortcode": self.contest.business_owner.shortcode,
                "ref_shortcode": self.ref_shortcode,
                "contest_id": self.contest.id,
            },
        )


# @receiver(post_save, sender=Referral)
# def update_referral_count(sender, created, instance, **kwargs):
#     if created:
#         print('Before: ', instance.business_owner.referral_count)
#         instance.business_owner.referral_count += 1
#         instance.business_owner.save()
#         print('After: ', instance.business_owner.referral_count)


class Guest(models.Model):
    referral = models.ForeignKey(
        Referral, on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        Contest,
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
        # self.referral.guest_count += 1
        super(Guest, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-id",)


# @receiver(post_save, sender=Guest)
# def update_guest_count(sender, created, instance, **kwargs):
#     if created:
#         print('Before guest_count: ', instance.referral.guest_count)
#         instance.referral.guest_count += 1
#         instance.referral.save()
#         print('After: guest_count ', instance.referral.guest_count)

