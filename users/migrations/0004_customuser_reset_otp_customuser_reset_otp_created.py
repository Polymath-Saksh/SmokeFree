# Generated by Django 5.0.7 on 2025-04-29 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_customuser_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="reset_otp",
            field=models.CharField(blank=True, default=None, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="reset_otp_created",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
