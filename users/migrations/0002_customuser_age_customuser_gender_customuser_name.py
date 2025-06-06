# Generated by Django 5.0.7 on 2025-04-29 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="name",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
