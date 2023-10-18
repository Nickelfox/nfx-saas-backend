# Generated by Django 4.2.5 on 2023-10-18 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_company_invite_type"),
        ("department", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="department",
            name="company_id",
        ),
        migrations.AddField(
            model_name="department",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="company.company",
            ),
        ),
    ]