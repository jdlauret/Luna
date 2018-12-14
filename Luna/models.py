import os
import re
import json
import django
import datetime as dt
from dateutil.parser import parse
from django.db import models
from django.conf import settings

"""
Setup class with all column definitions

import class in Luna/admin.py
admin.site.register(<ClassName>) to Luna/admin.py

Then type in the following Command Prompt lines setup New Table

python manage.py makemigrations Luna
python manage.py sqlmigrate Luna 0001
python manage.py migrate
"""


class CareerPath(models.Model):
    # Department Codes
    # REAL_TIME_SCHEDULING = 'real_time_scheduling'
    CENTRAL_SCHEDULING = 'central_scheduling'
    CUSTOMER_SERVICE = 'customer_service'
    CUSTOMER_SOLUTIONS = 'customer_solutions'
    RECS_AND_REBATES = 'RECs_&_rebates'
    CUSTOMER_RELATIONS = 'customer_relations'

    # Function Codes
    INBOUND = 'inbound'
    AUXILIARY = 'auxiliary'
    SUPER_AGENT = 'super_agent'
    CUSTOMER_SOLUTIONS = 'customer_solutions'
    SERVICE = 'service'
    CUSTOMER_SOLUTIONS_ADMIN = 'customer_solutions_admin'
    TRANSFER = 'transfer'
    RESOLUTION = 'resolution'
    INBOUND_OUTBOUND = 'inbound_outbound'
    EMAIL_ADMIN = 'email_admin'
    DOCUMENTS = 'documents'

    # Position Codes
    REP_1 = 'rep_1'
    REP_2 = 'rep_2'
    REP_3 = 'rep_3'
    SPECIALIST_1 = 'specialist_1'
    SPECIALIST_2 = 'specialist_2'
    SPECIALIST_3 = 'specialist_3'
    TEAM_LEAD = 'team_lead'

    # Pay Tiers
    TIER_1_1 = 12.00
    TIER_2_1 = 13.00
    TIER_2_2 = 13.25
    TIER_2_3 = 13.75
    TIER_3_1 = 14.00
    TIER_3_2 = 14.25
    TIER_3_3 = 14.50

    DEPARTMENTS = (
        # (REAL_TIME_SCHEDULING, 'real time scheduling'),
        (CENTRAL_SCHEDULING, 'Central Scheduling'),
        (CUSTOMER_SERVICE, ''),
        (CUSTOMER_SOLUTIONS, ''),
        (RECS_AND_REBATES, ''),
        (CUSTOMER_RELATIONS, 'Customer Relations')
    )

    FUNCTIONS = (
        (INBOUND, ' - Inbound'),
        (AUXILIARY, ' - Auxiliary'),
        (SUPER_AGENT, ' - Super Agent'),
        (CUSTOMER_SOLUTIONS, 'Customer Solutions'),
        (SERVICE, ' - Service'),
        (CUSTOMER_SERVICE, 'Customer Service'),
        (TRANSFER, 'Transfer'),
        (RESOLUTION, 'Resolution'),
        (CUSTOMER_SOLUTIONS_ADMIN, 'Customer Solutions Admin'),
        (RECS_AND_REBATES, 'RECs & Rebates'),
        (INBOUND_OUTBOUND, ' - Inbound/Outbound'),
        (EMAIL_ADMIN, ' - Email Admin'),
        (DOCUMENTS, ' - Documents'),
    )

    POSITIONS = (
        (REP_1, 'Rep 1'),
        (REP_2, 'Rep 2'),
        (REP_3, 'Rep 3'),
        (SPECIALIST_1, 'Specialist 1'),
        (SPECIALIST_2, 'Specialist 2'),
        (SPECIALIST_3, 'Specialist 3'),
        (TEAM_LEAD, 'Team Lead'),
    )

    PAY_RATES = (
        (TIER_1_1, '$12.00'),
        (TIER_2_1, '$13.00'),
        (TIER_2_2, '$13.25'),
        (TIER_2_3, '$13.75'),
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
        (2.5, '2.5%'),
        (3, '3%'),
        (5, '5%'),
        (7, '7%'),
        (10, '10%'),
        (20, '20%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (75, '75%'),
        (80, '80%'),
        (85, '85%'),
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
    qa = models.FloatField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    productivity = models.FloatField(
        choices=PERCENTAGES,
        null=True,
        blank=True
    )
    aht = models.FloatField(
        null=True,
        blank=True,
    )
    aph = models.FloatField(
        null=True,
        blank=True
    )
    adh = models.FloatField(
        null=True,
        blank=True,
        choices=PERCENTAGES,
    )
    availability = models.FloatField(
        null=True,
        blank=True
    )
    error_rate = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    efficiency = models.FloatField(
        null=True,
        blank=True
    )
    duration = models.FloatField(
        default=90.0,
        blank=True,
        null=True,
    )
    nps = models.FloatField(
        null=True,
        blank=True
    )
    field_qa_nps_score = models.FloatField(
        null=True,
        blank=True
    )
    job_description = models.TextField()

    def position_display(self):
        return dict(CareerPath.POSITIONS)[self.position]

    def department_display(self):
        return dict(CareerPath.DEPARTMENTS)[self.department]

    def function_display(self):
        return dict(CareerPath.FUNCTIONS)[self.function]

    def pay_rate_display(self):
        return dict(CareerPath.PAY_RATES)[self.pay_rate]

    def tier_display(self):
        return dict(CareerPath.TIER_LEVELS)[self.tier_level]

    def qa_display(self):
        return dict(CareerPath.PERCENTAGES)[self.qa]

    def adh_display(self):
        return dict(CareerPath.PERCENTAGES)[self.adh]

    def availability_display(self):
        return dict(CareerPath.PERCENTAGES)[self.availability]

    def efficiency_display(self):
        return dict(CareerPath.PERCENTAGES)[self.efficiency]

    # def error_rate_display(self):
    #     return dict(CareerPath.ERROR_RATE)[self.error_rate]

    def productivity_display(self):
        return dict(CareerPath.PERCENTAGES)[self.productivity]


class AutomatorTask(models.Model):
    # TODO create AutomatorTask model once requirements are scoped out
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
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    submit_date = models.DateField(default=django.utils.timezone.now)

class buyout_calc_model(models.Model):
    transfer_buyout = models.DecimalField(max_digits=3, decimal_places=2)
    default_price = models.DecimalField(max_digits=3, decimal_places=2)
