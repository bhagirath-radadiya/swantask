# Generated by Django 3.0.8 on 2021-01-22 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0002_auto_20210122_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to='product/'),
            preserve_default=False,
        ),
    ]
