# Generated by Django 2.0.6 on 2018-09-15 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0023_auto_20180914_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpath',
            name='aht',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]