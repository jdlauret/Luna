import datetime as dt
from django.db import models
from django.utils import timezone

"""
Setup class with all column definitions

import class in Luna/admin.py
admin.site.register(<ClassName>) to Luna/admin.py

Then type in the following Command Prompt lines setup New Table

python manage.py makemigrations Luna
python manage.py sqlmigration Luna 0001
python manage.py migrate
"""


class CareerPath(models.Model):
    # Department Codes
    REAL_TIME_SCHEDULING = 'real_time_scheduling'
    CUSTOMER_SERVICE = 'customer_service'
    CUSTOMER_SOLUTIONS = 'customer_solutions'
    RECS_AND_REBATES = 'recs_and_rebates'
    RELATIONS = 'relations'

    # Function Codes
    INBOUND = 'inbound'
    AUXILIARY = 'auxiliary'
    SUPER_AGENT = 'super_agent'
    SERVICE = 'service'
    SPECIALIST_1 = 'specialist_1'
    INBOUND_OUTBOUND = 'inbound_outbound'
    EMAIL_ADMIN = 'email_admin'
    DOCUMENTS = 'documents'

    # Position Codes
    REP_1 = 'representative_1'
    REP_2 = 'representative_2'
    REP_3 = 'representative_3'
    SPECIALIST_2 = 'specialist_2'
    SPECIALIST_3 = 'specialist_3'
    TEAM_LEAD = 'team_lead'

    # Pay Tiers
    TIER_1_1 = 12.00
    TIER_2_1 = 13.00
    TIER_2_2 = 13.25
    TIER_2_3 = 13.50
    TIER_3_1 = 14.00
    TIER_3_2 = 14.25
    TIER_3_3 = 14.50

    DEPARTMENTS = (
        (REAL_TIME_SCHEDULING, 'Real Time Scheduling'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (CUSTOMER_SOLUTIONS, 'Customer Solutions'),
        (RECS_AND_REBATES, 'RECs & Rebates'),
        (RELATIONS, 'Relations')
    )

    FUNCTIONS = (
        (INBOUND, 'Inbound'),
        (AUXILIARY, 'Auxiliary'),
        (SUPER_AGENT, 'Super Agent'),
        (SERVICE, 'Service'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (SPECIALIST_1, 'Specialist 1'),
        (RECS_AND_REBATES, 'RECs & Rebates'),
        (INBOUND_OUTBOUND, 'Inbound / Outbound'),
        (EMAIL_ADMIN, 'Email Admins'),
        (DOCUMENTS, 'Documents'),
    )

    POSITIONS = (
        (REP_1, 'Representative 1'),
        (REP_2, 'Representative 2'),
        (REP_3, 'Representative 3'),
        (SPECIALIST_1, 'Specialist 1'),
        (SPECIALIST_2, 'Specialist 2'),
        (SPECIALIST_3, 'Specialist 3'),
        (TEAM_LEAD, 'Team Lead'),
    )

    PAY_RATES = (
        (TIER_1_1, '$12.00'),
        (TIER_2_1, '$13.00'),
        (TIER_2_2, '$13.25'),
        (TIER_2_3, '$13.50'),
        (TIER_3_1, '$14.00'),
        (TIER_3_2, '$14.25'),
        (TIER_3_3, '$14.50'),
    )

    TIER_LEVELS = (
        (1.1, 'Tier 1.1'),
        (2.1, 'Tier 2.1'),
        (2.2, 'Tier 2.2'),
        (2.3, 'Tier 2.3'),
        (3.1, 'Tier 3.1'),
        (3.2, 'Tier 3.2'),
        (3.3, 'Tier 3.3'),
    )

    PERCENTAGES = (
        (0, '0%'),
        (10, '10%'),
        (20, '20%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (75, '75%'),
        (80, '80%'),
        (90, '90%'),
        (100, '100%'),
    )

    tier_level = models.FloatField(
        choices=TIER_LEVELS
    )
    pay_rate = models.FloatField(
        choices=PAY_RATES
    )
    department = models.CharField(
        max_length=200,
        choices=DEPARTMENTS,
    )
    function = models.CharField(
        max_length=200,
        choices=FUNCTIONS,
        null=True,
        blank=True,
    )
    position = models.CharField(
        max_length=200,
        choices=POSITIONS
    )
    qa = models.IntegerField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    productivity = models.IntegerField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    aht = models.IntegerField(
        null=True,
        blank=True
    )
    aph = models.IntegerField(
        null=True,
        blank=True
    )
    adh = models.IntegerField(
        null=True,
        blank=True
    )
    availability = models.IntegerField(
        null=True,
        blank=True
    )
    error_rate = models.IntegerField(
        null=True,
        blank=True
    )
    efficiency = models.IntegerField(
        null=True,
        blank=True
    )
    duration = models.IntegerField(
        default=90
    )
    nps = models.IntegerField(
        null=True,
        blank=True
    )
    field_qa_nps_score = models.IntegerField(
        null=True,
        blank=True
    )
    job_description = models.TextField()


class AutomatorTask(models.Model):
    # TODO create AutomatorTask model once requirments are scoped out
    day = models.DateField(
        blank=True,
        null=True
    )
    hour = models.IntegerField(
        blank=True,
        null=True
    )

class Idea(models.Model):

    concept = models.TextField()
    up_votes = models.IntegerField(
        default=0
    )
    down_votes = models.IntegerField(
        default=0
    )
    submit_date = models.DateField(
        default=timezone.now()
    )