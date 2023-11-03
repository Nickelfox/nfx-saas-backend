# Generated by Django 4.2.5 on 2023-10-18 13:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("notes", models.TextField()),
                ("status", models.CharField(max_length=255)),
                (
                    "project_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.projectmember",
                    ),
                ),
            ],
            options={
                "verbose_name": "Schedule",
                "verbose_name_plural": "Schedules",
                "ordering": ["-created_at"],
            },
        ),
    ]