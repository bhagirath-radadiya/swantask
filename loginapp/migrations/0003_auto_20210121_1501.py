# Generated by Django 3.0.8 on 2021-01-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0002_auto_20210121_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=250),
        ),
    ]
