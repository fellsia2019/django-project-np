# Generated by Django 5.1.4 on 2025-01-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_image_webp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image_webp',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
