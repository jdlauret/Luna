# Generated by Django 2.0.5 on 2018-10-08 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('P_Tracker', '0007_auto_20181008_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_name',
            name='full_name',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='meeting_time',
            name='auth_employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='P_Tracker.Auth_Employee'),
        ),
        migrations.AlterField(
            model_name='project_name',
            name='badge_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='P_Tracker.Auth_Employee'),
        ),
        migrations.AlterField(
            model_name='project_time',
            name='auth_employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='P_Tracker.Auth_Employee'),
        ),
        migrations.AlterField(
            model_name='training_time',
            name='auth_employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='P_Tracker.Auth_Employee'),
        ),
    ]
