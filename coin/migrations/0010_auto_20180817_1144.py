# Generated by Django 2.0.7 on 2018-08-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0009_auto_20180813_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='leaders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='To Be Filled in Later', max_length=100)),
                ('badge_num', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='redeemed',
            field=models.IntegerField(default=0),
        ),
    ]