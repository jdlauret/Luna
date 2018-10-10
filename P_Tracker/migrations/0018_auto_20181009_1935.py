# Generated by Django 2.0.5 on 2018-10-10 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('P_Tracker', '0017_auto_20181009_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting_time',
            old_name='total',
            new_name='total_time',
        ),
        migrations.RenameField(
            model_name='project_time',
            old_name='total',
            new_name='total_time',
        ),
        migrations.RenameField(
            model_name='training_time',
            old_name='total',
            new_name='total_time',
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
