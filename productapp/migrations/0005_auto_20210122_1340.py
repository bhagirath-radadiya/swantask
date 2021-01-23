# Generated by Django 3.0.8 on 2021-01-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0004_auto_20210122_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('puma', 'Puma'), ('adidas', 'Adidas'), ('woodland', 'Woodland'), ('red tap', 'Red Tap'), ('bata', 'Bata')], max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('sneakers', 'Sneakers'), ('loafers', 'Loafers'), ('derby', 'Derby')], max_length=10),
        ),
    ]