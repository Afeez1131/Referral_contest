from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import RegexValidator
from autoslug import AutoSlugField
from django.utils import timezone
from django.urls import reverse


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, full_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be given a Staff status")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be given a superuser status")
        # email = self.normalize_email(email)
        return self.create_user(username, full_name, password, **other_fields)

    def create_user(self, username, full_name, password, **other_fields):
        # email = self.normalize_email(email)
        # if not email:
        #     raise ValueError('You must provide an E-mail address.')

        if not full_name:
            raise ValueError("You must provide your full name.")

        user = self.model(
            username=username, full_name=full_name, password=password, **other_fields
        )

        user.set_password(password)
        user.save()
        return user


class BusinessOwner(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="username", max_length=150, unique=True)
    business_name = models.CharField(verbose_name="business name", max_length=150)
    phone_regex = RegexValidator(
        regex="^[0]\d{10}$", message="Phone number should be in the format: 08105506606"
    )
    phone_number = models.CharField(
        max_length=11, validators=[phone_regex], unique=True
    )
    full_name = models.CharField(max_length=150)
    shortcode = AutoSlugField(populate_from="business_name")
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "full_name", "business_name"]

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ("-id",)

    def get_absolute_url(self):
        return reverse("owner_home", kwargs={"shortcode": self.shortcode})

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
