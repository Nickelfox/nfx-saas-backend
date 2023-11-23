# Generated by Django 4.2.5 on 2023-11-17 04:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedule", "0003_schedule_assigned_hour"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="schedule_type",
            field=models.CharField(
                choices=[("WORK", "Work"), ("TIME_OFF", "Time Off")],
                default="WORK",
                max_length=40,
            ),
        ),
    ]
