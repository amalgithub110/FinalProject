# Generated by Django 5.2.2 on 2025-06-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_otp_varified_user_otp_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
