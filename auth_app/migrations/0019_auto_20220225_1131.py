# Generated by Django 3.2 on 2022-02-25 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0018_alter_contest_starting_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contest",
            name="duration",
        ),
        migrations.AlterField(
            model_name="contest",
            name="ending_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="contest",
            name="starting_date",
            field=models.DateTimeField(),
        ),
    ]
