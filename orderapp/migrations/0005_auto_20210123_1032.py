# Generated by Django 3.0.8 on 2021-01-23 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0004_order_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(null=True),
        ),
    ]
