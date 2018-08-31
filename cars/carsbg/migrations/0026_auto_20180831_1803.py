# Generated by Django 2.0.7 on 2018-08-31 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsbg', '0025_auto_20180831_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date', 'user']},
        ),
        migrations.AlterModelOptions(
            name='object',
            options={'ordering': ['rating', 'name']},
        ),
        migrations.AddField(
            model_name='comment',
            name='rate',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
