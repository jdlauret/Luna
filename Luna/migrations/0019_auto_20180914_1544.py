# Generated by Django 2.0.6 on 2018-09-14 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0018_auto_20180914_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpath',
            name='position',
            field=models.CharField(choices=[('representative_1', 'Representative 1'), ('representative_2', 'Representative 2'), ('representative_3', 'Representative 3'), ('specialist_1', 'Specialist 1'), ('specialist_2', 'Specialist 2'), ('specialist_3', 'Specialist 3'), ('team_lead', 'Team Lead')], max_length=200),
        ),
    ]