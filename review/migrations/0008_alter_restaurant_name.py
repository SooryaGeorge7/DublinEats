# Generated by Django 3.2.19 on 2023-07-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_alter_restaurant_restaurantid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.TextField(),
        ),
    ]
