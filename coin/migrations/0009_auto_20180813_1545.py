# Generated by Django 2.0.7 on 2018-08-13 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0008_auto_20180813_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_id',
            name='edited',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]