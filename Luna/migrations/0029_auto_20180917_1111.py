# Generated by Django 2.0.6 on 2018-09-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0028_auto_20180917_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpath',
            name='adh',
            field=models.FloatField(blank=True, choices=[(0, '0%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='availability',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='duration',
            field=models.FloatField(blank=True, default=90, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='efficiency',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='error_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='field_qa_nps_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='nps',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='productivity',
            field=models.IntegerField(blank=True, choices=[(0, '0%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='qa',
            field=models.IntegerField(blank=True, choices=[(0, '0%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
    ]