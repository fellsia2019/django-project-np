# Generated by Django 5.1.4 on 2025-01-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_alter_article_image_alter_initiative_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_webp',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='initiative',
            name='image_webp',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
