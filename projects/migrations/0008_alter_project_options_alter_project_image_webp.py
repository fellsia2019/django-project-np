# Generated by Django 5.1.4 on 2025-01-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_image_webp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterField(
            model_name='project',
            name='image_webp',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
