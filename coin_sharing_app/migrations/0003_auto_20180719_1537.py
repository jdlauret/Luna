# Generated by Django 2.0.7 on 2018-07-19 21:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coin_sharing_app', '0002_auto_20180719_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='status_coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AGENT_NAME', models.CharField(max_length=100)),
                ('BADGE_ID', models.IntegerField(blank=True, null=True)),
                ('COIN_GIVE', models.IntegerField(blank=True, null=True)),
                ('COIN_RECEIVED', models.IntegerField(blank=True, null=True)),
                ('COIN_TOTAL', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='transaction_coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FROM_BADGEID', models.IntegerField(blank=True, null=True)),
                ('TO_BADGEID', models.IntegerField(blank=True, null=True)),
                ('COIN_TO_GIVE', models.IntegerField(blank=True, null=True)),
                ('REDEMPTION_CODE', models.CharField(blank=True, max_length=12, null=True)),
                ('NOTE', models.TextField(blank=True, null=True)),
                ('test', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='coin_stat',
        ),
        migrations.DeleteModel(
            name='coin_trans',
        ),
    ]
