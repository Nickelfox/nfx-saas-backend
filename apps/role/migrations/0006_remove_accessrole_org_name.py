# Generated by Django 4.2.5 on 2023-11-30 08:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("role", "0005_alter_accessrole_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accessrole",
            name="org_name",
        ),
    ]
