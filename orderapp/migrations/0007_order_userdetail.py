# Generated by Django 3.0.8 on 2021-01-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0006_order_grandtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='userDetail',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
