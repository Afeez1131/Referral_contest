# Generated by Django 3.2 on 2022-09-13 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0027_contest_referral_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='referral_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]