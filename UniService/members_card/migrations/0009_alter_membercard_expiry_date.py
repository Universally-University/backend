# Generated by Django 4.2.6 on 2023-10-15 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members_card', '0008_alter_membercard_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membercard',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2024, 10, 14), verbose_name='Expires on'),
        ),
    ]
