# Generated by Django 3.0.8 on 2021-01-22 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='availibility',
            new_name='quantity',
        ),
    ]
