# Generated by Django 3.2.19 on 2023-07-30 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_alter_restaurant_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ambience',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='customer_service',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='location',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='taste',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='value_for_money',
            field=models.IntegerField(default=0),
        ),
    ]