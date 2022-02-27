# Generated by Django 3.2 on 2022-01-20 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base_app", "0005_remove_businessowner_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guest",
            name="business",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="guest_business",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="referral",
            name="business_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="refer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
