# Generated by Django 4.2.5 on 2023-11-30 07:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_company_invite_type"),
        ("role", "0004_accessrole_org_name_alter_accessrole_name_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="accessrole",
            unique_together={("name", "company")},
        ),
    ]