# Generated by Django 3.2 on 2022-02-11 16:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_app", "0017_alter_guest_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guest",
            name="phone_number",
            field=models.CharField(
                max_length=13,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '2348105506070'. Up to 13 digits allowed.",
                        regex="^234\\d{10}$",
                    )
                ],
            ),
        ),
    ]
