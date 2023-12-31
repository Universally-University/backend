# Generated by Django 4.2.6 on 2023-10-08 04:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members_card", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="membercard",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Active Card"),
        ),
        migrations.AlterField(
            model_name="membercard",
            name="expiry_date",
            field=models.DateField(
                default=datetime.date(2024, 10, 7), verbose_name="Expires on"
            ),
        ),
    ]
