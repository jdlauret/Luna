# Generated by Django 2.0.7 on 2018-08-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0010_auto_20180817_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_id',
            name='terminated',
            field=models.IntegerField(default=0),
        ),
    ]
