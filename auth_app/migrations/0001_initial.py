# Generated by Django 3.2 on 2022-01-20 11:41

import autoslug.fields
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessOwner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="username"
                    ),
                ),
                (
                    "business_name",
                    models.CharField(max_length=150, verbose_name="business name"),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number should be in the format: 08105506606",
                                regex="^[0]\\d{10}$",
                            )
                        ],
                    ),
                ),
                ("full_name", models.CharField(max_length=150)),
                (
                    "shortcode",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="business_name"
                    ),
                ),
                ("start_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
    ]
