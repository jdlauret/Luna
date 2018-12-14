from __future__ import unicode_literals
from datetime import datetime as dt, timedelta
import pytz
from django.db import models
from dateutil import parser


class Soft_Skills_Manager(models.Manager):

	@classmethod
	def add_soft_skills_id(self, post_data):
		error = []
		print(post_data)

# 		ADDS A SOFT SKILL ID TO EMPLOYEE BADGE ID
# 		temp = Agent_Skills(
# 			badge_id_id = post_data[''],
# 			skill_id_id= post_data[''],
# 		)

class Career_Path(models.Model):
	# DEPARTMENT CODES
	CENTRAL_SCHEDULING = 'central_scheduling'
	CUSTOMER_SERVICE = 'customer_service'
	CUSTOMER_SOLUTIONS = 'customer_solutions'
	RECS_AND_REBATES = 'RECs_&_rebates'
	CUSTOMER_RELATIONS = 'customer_relations'

	# FUNCTION CODES
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
		(CENTRAL_SCHEDULING, 'Central Scheduling'),
		(CUSTOMER_SERVICE, 'Customer Service'),
		(CUSTOMER_SOLUTIONS, 'Customer Solutions'),
		(RECS_AND_REBATES, 'RECs & Rebates'),
		(CUSTOMER_RELATIONS, 'Customer Relations'),
	)

	FUNCTIONS = (
		(INBOUND, 'Inbound'),
		(AUXILIARY, 'Auxiliary'),
		(SUPER_AGENT, 'Super Agent'),
		(CUSTOMER_SOLUTIONS, 'Customer Solutions'),
		(SERVICE, 'Service'),
		(CUSTOMER_SERVICE, 'Customer Service'),
		(TRANSFER, 'Transfer'),
		(RESOLUTION, 'Resolution'),
		(CUSTOMER_SOLUTIONS_ADMIN, 'Customer Solutions Admin'),
		(RECS_AND_REBATES, 'RECs & Rebates'),
		(INBOUND_OUTBOUND, 'Inbound/Outbound'),
		(EMAIL_ADMIN, 'Email Admin'),
		(DOCUMENTS, 'Documents'),
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
		(1, '1%'),
		(2, '2%'),
		(2.5, '2.5%'),
		(3, '3%'),
		(4, '4%'),
		(5, '5%'),
		(6, '6%'),
		(7, '7%'),
		(8, '8%'),
		(9, '9%'),
		(10, '10%'),
		(15, '15%'),
		(20, '20%'),
		(25, '25%'),
		(30, '30%'),
		(35, '35%'),
		(40, '40%'),
		(45, '45%'),
		(50, '50%'),
		(55, '55%'),
		(60, '60%'),
		(65, '65%'),
		(70, '70%'),
		(75, '75%'),
		(80, '80%'),
		(85, '85%'),
		(90, '90%'),
		(95, '95%'),
		(100, '100%'),
	)

	team = models.CharField(max_length=200, choices=DEPARTMENTS)
	sub_team = models.CharField(max_length=200, choices=FUNCTIONS, null=True, blank=True)
	tier = models.CharField(max_length=200, choices=POSITIONS)
	tier_level = models.FloatField(choices=TIER_LEVELS)
	description = models.CharField(max_length=1000)
	qa = models.FloatField(choices=PERCENTAGES, null=True, blank=True)
	productivity = models.FloatField(choices=PERCENTAGES, null=True, blank=True)
	aht = models.FloatField(null=True, blank=True)
	aph = models.FloatField(null=True, blank=True)
	adh = models.FloatField(null=True, blank=True, choices=PERCENTAGES)
	availability = models.FloatField(null=True, blank=True)
	error_rate = models.CharField(max_length=500, null=True, blank=True)
	efficiency = models.FloatField(null=True, blank=True)
	duration = models.FloatField(default=90.0, blank=True, null=True)
	nps = models.FloatField(null=True, blank=True)
	field_qa_nps_score = models.FloatField(null=True, blank=True)
	pay_rate = models.FloatField(choices=PAY_RATES)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	edited_at = models.DateTimeField(null=True)


class Employee_List(models.Model):
	badge_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	business_title = models.CharField(max_length=500)
	supervisor_badge = models.IntegerField(null=True)
	supervisor_name = models.CharField(max_length=200)
	hire_date = models.DateTimeField(null=True)
	team = models.CharField(max_length=200)
	sub_team = models.CharField(max_length=200, null=True)
	tier = models.CharField(max_length=200)
	terminated = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	edited_at = models.DateTimeField(null=True)

class Agent_Skills(models.Model):
	badge_id = models.ForeignKey(Employee_List, on_delete=models.CASCADE)
	skill_id = models.ForeignKey(Career_Path, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	edited_at = models.DateTimeField(null=True)

# TODO CREATE QUERY FROM SNOWFLAKE, PULL THE SUPERVISOR LIST AND THEN SET VALUE TO BADGE ID