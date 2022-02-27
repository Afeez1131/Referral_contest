# Generated by Django 3.2 on 2022-02-11 16:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_app", "0015_auto_20220211_1832"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guest",
            name="phone_number",
            field=models.CharField(
                max_length=11,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '2348105506070'. Up to 11 digits allowed.",
                        regex="^0\\d{10}$",
                    )
                ],
            ),
        ),
    ]
