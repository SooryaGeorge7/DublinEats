# Generated by Django 3.2.19 on 2023-07-30 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_auto_20230730_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='category',
            field=models.TextField(default='None'),
        ),
    ]