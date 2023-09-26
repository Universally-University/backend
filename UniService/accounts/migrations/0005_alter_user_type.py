# Generated by Django 4.2.4 on 2023-09-26 04:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_user_groups_user_is_staff_user_is_superuser_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="type",
            field=models.CharField(
                choices=[
                    ("U", "Undergraduate"),
                    ("P", "Postgraduate"),
                    ("S", "Staff"),
                    ("A", "Admin"),
                ],
                max_length=30,
                verbose_name="Type",
            ),
        ),
    ]