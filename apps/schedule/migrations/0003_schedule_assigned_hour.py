# Generated by Django 4.2.5 on 2023-11-02 05:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_remove_schedule_status_alter_schedule_end_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='assigned_hour',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]