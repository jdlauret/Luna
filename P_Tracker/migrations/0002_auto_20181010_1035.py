# Generated by Django 2.0.5 on 2018-10-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('P_Tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting_time',
            name='total_time',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='project_time',
            name='total_time',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='training_time',
            name='total_time',
            field=models.CharField(max_length=200, null=True),
        ),
    ]