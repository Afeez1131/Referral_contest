# Generated by Django 3.2 on 2022-01-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_app", "0007_delete_businessowner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referral",
            name="refer_message",
            field=models.CharField(
                default="Hello, i am currently participating in a referral contest, kindly vote for me using this link ",
                max_length=100,
            ),
        ),
    ]
