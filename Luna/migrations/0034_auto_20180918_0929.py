# Generated by Django 2.0.5 on 2018-09-18 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0033_careerpath_error_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpath',
            name='adh',
            field=models.FloatField(blank=True, choices=[(0, '0%'), (2.5, '2.5%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='department',
            field=models.CharField(choices=[('central_scheduling', 'Central Scheduling'), ('customer_service', ''), ('customer_solutions', ''), ('RECs_&_rebates', ''), ('relations', 'Relations')], max_length=200),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='error_rate',
            field=models.CharField(choices=[(7, '7% over a rolling 1 month period OR ≤ 10 errors per week '), (5, '5% over a rolling 1 month period OR ≤ 10 errors per week '), (2, '2.5% over a rolling 1 month period OR ≤ 10 errors per week '), (0, '')], default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='function',
            field=models.CharField(blank=True, choices=[('inbound', 'Inbound'), ('auxiliary', 'Auxiliary'), ('super_agent', 'Super Agent'), ('customer_solutions', 'Customer Solutions'), ('service', 'Service'), ('customer_service', 'Customer Service'), ('transfer', 'Transfer'), ('resolution', 'Resolution'), ('customer_solutions_admin', 'Customer Solutions Admin'), ('RECs_&_rebates', 'RECs & Rebates'), ('inbound_outbound', 'Inbound / Outbound'), ('email_admin', 'Email Admins'), ('documents', 'Documents')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='position',
            field=models.CharField(choices=[('rep_1', 'Rep 1'), ('rep_2', 'Rep 2'), ('rep_3', 'Rep 3'), ('specialist_1', 'Specialist 1'), ('specialist_2', 'Specialist 2'), ('specialist_3', 'Specialist 3'), ('team_lead', 'Team Lead')], max_length=200),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='productivity',
            field=models.FloatField(blank=True, choices=[(0, '0%'), (2.5, '2.5%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
        migrations.AlterField(
            model_name='careerpath',
            name='qa',
            field=models.FloatField(blank=True, choices=[(0, '0%'), (2.5, '2.5%'), (3, '3%'), (5, '5%'), (7, '7%'), (10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (75, '75%'), (80, '80%'), (85, '85%'), (90, '90%'), (100, '100%')], null=True),
        ),
    ]
