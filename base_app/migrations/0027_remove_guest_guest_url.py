# Generated by Django 3.2 on 2022-03-06 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0026_auto_20220306_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='guest_url',
        ),
    ]
