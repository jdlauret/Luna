# Generated by Django 2.0.5 on 2018-10-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('P_Tracker', '0004_auto_20181012_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting_time',
            name='reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project_time',
            name='reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='training_time',
            name='reject',
            field=models.BooleanField(default=False),
        ),
    ]