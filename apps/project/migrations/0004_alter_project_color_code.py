# Generated by Django 4.2.5 on 2023-12-13 12:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0003_alter_project_color_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="color_code",
            field=models.CharField(
                blank=True,
                choices=[
                    ("#F10982", "Warm Red"),
                    ("#FF0000", "Red"),
                    ("#FF7034", "Orange"),
                    ("#800000", "Maroon"),
                    ("#4169e1", "Royal Blue"),
                    ("#57f287", "Light Green"),
                ],
                default=None,
                max_length=40,
                null=True,
            ),
        ),
    ]