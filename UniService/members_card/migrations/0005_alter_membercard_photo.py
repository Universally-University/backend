# Generated by Django 4.2.6 on 2023-10-08 06:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members_card", "0004_alter_membercard_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membercard",
            name="photo",
            field=models.CharField(
                blank=True, max_length=10000, null=True, verbose_name="User Image"
            ),
        ),
    ]
