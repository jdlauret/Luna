from __future__ import unicode_literals
import datetime as dt
from django.db import models

# THIS ALLOWS PEOPLE ACESS TO THE PRODUCTIVITY TRACKER
class auth_employee (models.Model):

	# FUNCTION CODE
	MANAGER = 'manager'
	SUPER = 'super'
	TL = 'tl'
	EMPLOYEE = 'employee'

	FUNCTIONS = (
		(MANAGER, 'Manager'),
		(SUPER, 'Supervisor'),
		(TL, 'Team Lead'),
		(EMPLOYEE, 'Employee'),
	)

	badge_id = models.AutoField(primary_key=True)
	full_name = models.CharField(max_length=200)
	authority = models.CharField(
		max_length=200,
		choices=FUNCTIONS,
		null=True,
		blank=True,
	)
	supervisor = models.CharField(
		max_length=200,
		null=True,
		blank=True,
	)

# INDIVIDUAL TRACKER-
class employee_tracker (models.Model) :
	employee_id = models.ForeignKey(auth_employee, on_delete=models.CASCADE)
	activity = models.DecimalField(max_digits=5, decimal_places=2)
	project_time = models.DecimalField(max_digits=5, decimal_places=2)

class project(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField
	who_approved = models.CharField(max_length=200)
	super_stamp = models.CharField(max_length=200)
	start_date = models.DateTimeField(max_length=200)
	end_date = models.DateTimeField()

# Hours Worked
# Breaks
# Activity
# Meeting
# Huddle
# Project Time
# Productivity
# Activity Count

