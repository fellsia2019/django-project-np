# Generated by Django 5.1.4 on 2025-03-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_project_detail_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="image_webp",
        ),
        migrations.RemoveField(
            model_name="initiative",
            name="image_webp",
        ),
        migrations.RemoveField(
            model_name="project",
            name="image_webp",
        ),
        migrations.AddField(
            model_name="project",
            name="image_detail",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
