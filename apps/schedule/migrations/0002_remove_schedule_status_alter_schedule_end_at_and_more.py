# Generated by Django 4.2.5 on 2023-11-02 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='status',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_at',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_at',
            field=models.DateField(),
        ),
    ]
