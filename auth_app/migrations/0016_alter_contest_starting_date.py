# Generated by Django 3.2 on 2022-02-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0015_alter_contest_starting_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contest",
            name="starting_date",
            field=models.DateTimeField(blank=True),
        ),
    ]
