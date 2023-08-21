# Generated by Django 4.2.4 on 2023-08-18 04:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Staff ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="Last Name"),
                ),
                ("dob", models.DateField(verbose_name="Date of Birth")),
                ("contact", models.CharField(max_length=100, verbose_name="Contact")),
                ("address", models.CharField(max_length=300, verbose_name="Address")),
            ],
            options={
                "verbose_name": "Staff",
                "verbose_name_plural": "Staffs",
            },
        ),
    ]
