# Generated by Django 3.0.8 on 2021-01-22 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderstatus',
            field=models.CharField(default='addtocart', max_length=10),
        ),
    ]
