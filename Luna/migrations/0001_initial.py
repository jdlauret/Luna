# Generated by Django 2.0.4 on 2018-05-07 21:36


from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [

    ]

    operations = [

        migrations.CreateModel(

            name='CareerPath',

            fields=[

                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('tier_level', models.FloatField(
                    choices=[(1.1, 'Tier 1.1'), (2.1, 'Tier 2.1'), (2.2, 'Tier 2.2'), (2.3, 'Tier 2.3'),
                             (3.1, 'Tier 3.1'), (3.2, 'Tier 3.2'), (3.3, 'Tier 3.3')])),

                ('pay_rate', models.FloatField(
                    choices=[(12.0, '$12.00'), (13.0, '$13.00'), (13.25, '$13.25'), (13.5, '$13.50'), (14.0, '$14.00'),
                             (14.25, '$14.25'), (14.5, '$14.50')])),

                ('department', models.CharField(choices=[('RTS', 'Real Time Scheduling'), ('CSR', 'Customer Service'),
                                                         ('CSO', 'Customer Solutions'), ('RAR', 'RECs & Rebates'),
                                                         ('REL', 'Relations')], max_length=3)),

                ('function', models.CharField(
                    choices=[('IB', 'Inbound'), ('AUX', 'Auxiliary'), ('SA', 'Super Agent'), ('SER', 'Service'),
                             ('CSR', 'Customer Service'), ('SP1', 'Specialist 1'), ('SA', 'Super Agent'),
                             ('RAR', 'RECs and Rebates'), ('IBO', 'Inbound / Outbound'), ('EA', 'Email Admins'),
                             ('DOC', 'Documents')], max_length=200)),

                ('qa', models.IntegerField(blank=True, choices=[(60, '60%'), (70, '70%'), (80, '80%')])),

                ('aht', models.IntegerField(blank=True)),

                ('aph', models.IntegerField(blank=True)),

                ('adh', models.IntegerField(blank=True)),

                ('availability', models.IntegerField(blank=True)),

                ('error_rate', models.IntegerField(blank=True)),

                ('efficiency', models.IntegerField(blank=True)),

                ('duration', models.IntegerField(default=90)),

                ('nps', models.IntegerField(blank=True)),

                ('job_description', models.TextField()),

            ],

        ),

    ]
