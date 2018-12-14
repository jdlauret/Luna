# Generated by Django 2.0.5 on 2018-06-05 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0015_auto_20180517_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpath',
            name='adh',
            field=models.IntegerField(blank=True, choices=[(0, '0%'), (5, '5%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='aph',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='productivity',
            field=models.IntegerField(blank=True, choices=[(0, '0%'), (5, '5%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='qa',
            field=models.IntegerField(blank=True, choices=[(0, '0%'), (5, '5%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
    ]
