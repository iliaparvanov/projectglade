# Generated by Django 2.0.7 on 2018-07-14 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carsbg', '0009_auto_20180714_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='cardealer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carsbg.CarDealer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carsbg.Service'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
