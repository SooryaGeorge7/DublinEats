# Generated by Django 3.2.19 on 2023-06-30 12:12

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230630_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/dif9bjzee/image/upload/v1688126722/backgroud_upyhni.png', max_length=255, null=True, verbose_name='profile_images'),
        ),
    ]