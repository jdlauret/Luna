# Generated by Django 2.0.5 on 2018-06-05 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0017_auto_20180605_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='VcaasLogin',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('badge', models.IntegerField(blank=True, null=True)),
                ('incontact_id', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('department', models.CharField(blank=True, choices=[('cad', 'CAD'), ('click_support', 'Click Support'), ('collections', 'Collections'), ('customer_relations', 'Customer Relations'), ('customer_service', 'Customer Service'), ('customer_solutions', 'Customer Solution'), ('damage_resolutions', 'Damage Resolutions'), ('executive_resolutions', 'Executive Resolutions'), ('field_support', 'Field Support'), ('inspection_specialists', 'Inspection Specialist'), ('quality_assurance', 'Quality Assurance'), ('real_time_scheduling', 'Real Time Scheduling'), ('recs_and_rebates', 'RECs & Rebates'), ('sales_concierge', 'Sales Concierge'), ('solar_collections', 'Solar Collections'), ('workforce_management', 'Workforce Management')], max_length=200, null=True)),
                ('psuedo_number', models.IntegerField()),
                ('phone_number', models.IntegerField()),
                ('user_id', models.CharField(max_length=100)),
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('web_portal', models.CharField(max_length=10)),
                ('voice_mail_passcode', models.IntegerField(blank=True, null=True)),
                ('extension', models.IntegerField(blank=True, null=True)),
                ('voice_mail', models.BooleanField()),
                ('dnis_enabled', models.BooleanField()),
            ],
        ),
    ]
