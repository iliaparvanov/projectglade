# Generated by Django 2.0.7 on 2018-07-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsbg', '0015_auto_20180725_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardealer',
            name='lenOfRatings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='lenOfRatings',
            field=models.IntegerField(default=0),
        ),
    ]
