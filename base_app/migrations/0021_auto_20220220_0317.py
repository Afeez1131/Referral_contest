# Generated by Django 3.2 on 2022-02-20 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0014_auto_20220220_0317'),
        ('base_app', '0020_remove_guest_guest_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='business',
        ),
        migrations.AddField(
            model_name='guest',
            name='contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_guest', to='auth_app.contest'),
        ),
        migrations.AddField(
            model_name='referral',
            name='business_contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referral_contest', to='auth_app.contest'),
        ),
        migrations.AlterUniqueTogether(
            name='referral',
            unique_together={('business_contest', 'refer_name', 'phone_number')},
        ),
        migrations.RemoveField(
            model_name='referral',
            name='business_owner',
        ),
    ]
