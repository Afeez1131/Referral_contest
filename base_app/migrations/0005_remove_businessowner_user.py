# Generated by Django 3.2 on 2022-01-20 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_alter_businessowner_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessowner',
            name='user',
        ),
    ]