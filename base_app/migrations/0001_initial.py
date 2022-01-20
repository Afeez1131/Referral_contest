# Generated by Django 3.2 on 2022-01-18 08:21

import autoslug.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '08105506070'. Up to 11 digits allowed.", regex='^0\\d{10}$')])),
                ('shortcode', autoslug.fields.AutoSlugField(editable=False, populate_from='business_name')),
                ('broadcast_message', models.TextField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer_name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '08105506070'. Up to 11 digits allowed.", regex='^0\\d{10}$')])),
                ('ref_shortcode', models.CharField(blank=True, max_length=10, unique=True)),
                ('refer_message', models.CharField(default='Hello, i just signed up as a referral in your Referral Context, My name is ', max_length=100)),
                ('referral_url', models.CharField(blank=True, max_length=200, null=True)),
                ('business_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refer', to='base_app.businessowner')),
            ],
            options={
                'ordering': ('-id',),
                'unique_together': {('business_owner', 'refer_name', 'phone_number')},
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('guest_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '08105506070'. Up to 11 digits allowed.", regex='^0\\d{10}$')])),
                ('guest_count', models.IntegerField(default=0)),
                ('guest_url', models.CharField(blank=True, max_length=200)),
                ('guest_message', models.CharField(blank=True, max_length=100)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_business', to='base_app.businessowner')),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_referral', to='base_app.referral')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
