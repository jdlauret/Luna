# Generated by Django 2.0.5 on 2018-10-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('P_Tracker', '0003_auto_20181010_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting_time',
            name='edited_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='meeting_time',
            name='who_edited',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='project_time',
            name='edited_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='project_time',
            name='who_edited',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training_time',
            name='edited_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='training_time',
            name='who_edited',
            field=models.IntegerField(null=True),
        ),
    ]
