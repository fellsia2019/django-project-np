# Generated by Django 5.1.4 on 2025-01-09 12:15

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "projects",
            "0002_alter_article_options_alter_articlecategory_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="detail_text",
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]