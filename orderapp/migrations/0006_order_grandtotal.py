# Generated by Django 3.0.8 on 2021-01-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0005_auto_20210123_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='grandTotal',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
