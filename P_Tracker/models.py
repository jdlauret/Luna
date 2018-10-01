from __future__ import unicode_literals
import datetime as dt
from django.db import models

class auth_employee (models.Model):

	# FUNCTION CODE
	MANAGER = 'manager'
	SUPER = 'super'
	EMPLOYEE = 'employee'

	# SUPERVISOR CODE
	SUPER1 = ''
	SUPER2 = ''
	SUPER3 = ''
	SUPER4 = ''
	SUPER5 = ''

	FUNCTIONS = (
		(MANAGER, 'Manager'),
		(SUPER, 'Supervisor'),
		(EMPLOYEE, 'Employee'),
	)

	SUPERVISOR = (
		(SUPER1, 'Supervisor_1'),
		(SUPER2, 'Supervsior_2'),
		(SUPER3, 'Supervsior_3'),
		(SUPER4, 'Supervsior_4'),
		(SUPER5, 'Supervsior_5'),
	)

	badge_id = models.IntegerField()
	full_name = models.CharField(max_length=200)
	authority = models.CharField(
		max_length=200,
		choices=FUNCTIONS,
		null=True,
		blank=True,
	)
	supervisor = models.CharField(
		max_length=200,
		choices=SUPERVISOR,
		null=True,
		blank=True,
	)
