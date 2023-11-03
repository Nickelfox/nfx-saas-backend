# Generated by Django 4.2.5 on 2023-10-18 12:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("company", "0002_company_invite_type"),
        ("client", "0003_remove_client_company_id_client_company"),
        ("team", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("project_name", models.CharField(max_length=255)),
                (
                    "project_code",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "project_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("VARIABLE", "Variable By Hour"),
                            ("FIXED", "Fixed Fee"),
                            ("NON_BILLABLE", "Non Billable"),
                        ],
                        default=None,
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="client.client",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="company.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProjectMember",
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
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="team.team",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Member",
                "verbose_name_plural": "Project Members",
                "ordering": ["-created_at"],
            },
        ),
    ]