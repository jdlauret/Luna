# Generated by Django 2.0.4 on 2018-05-08 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0009_auto_20180508_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='automatortasks',
            name='hour',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='automatortasks',
            name='day',
            field=models.DateField(blank=True, null=True),
        ),
    ]
