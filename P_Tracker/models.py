from __future__ import unicode_literals
from datetime import datetime as dt
from dateutil import parser
import pytz
from django.db import models

# pytz.timezone('US/Mountain'

class trackerManager(models.Manager):
    @classmethod
    def proj_time_input(self, post_data, badge_id):
        errors = []
        project = int(post_data['project_name'])
        project = Project_Name.objects.get(pk=project)
        approved_by_id = int(post_data['approved_by'])
        approved_id = Auth_Employee.objects.get(badge_id=approved_by_id)

        temp = Project_Time(
            name=project.name,
            description=post_data['description'],
            who_approved_id=approved_by_id,
            who_approved_name=approved_id.full_name,
            start_time=dt.now(pytz.timezone('US/Mountain')),
            auth_employee_id=badge_id,
        )
        temp.save()

    @classmethod
    def proj_name_input(self, post_data, badge, full_name):
        errors = []
        if len(post_data) > 0 or len(badge) > 0:
            errors.append('No information was entered, please try again')
            return errors
        else:
            temp = Project_Name(
                name=post_data['create_project_name'],
                badge_id_id=int(badge),
                full_name=full_name,
            )
            temp.save()

    @classmethod
    def meeting_input(self, post_data, badge_id):
        errors = []
        if len(post_data) > 0 or len(badge_id) > 0:
            errors.append('No information was entered, please try again')
            return errors
        else:
            temp = Meeting_Time(
                name=post_data['meeting_name'],
                start_time=dt.now(pytz.timezone('US/Mountain')),
                auth_employee_id=badge_id,
            )
            temp.save()

    @classmethod
    def training_input(self, post_data, badge_id):
        errors = []
        if len(post_data) > 0 or len(badge_id) > 0:
            errors.append('No information was entered, please try again')
            return errors
        else:
            temp = Training_Time(
                name=post_data['training_name'],
                start_time=dt.now(pytz.timezone('US/Mountain')),
                auth_employee_id=badge_id,
            )
            temp.save()


# THIS ALLOWS PEOPLE ACcESS TO THE PRODUCTIVITY TRACKER
class Auth_Employee(models.Model):
    # FUNCTION CODE
    MANAGER = 'manager'
    SUPER = 'super'
    TL = 'tl'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'

    FUNCTIONS = (
        (MANAGER, 'Manager'),
        (SUPER, 'Supervisor'),
        (TL, 'Team Lead'),
        (EMPLOYEE, 'Employee'),
        (ADMIN, 'Admin')
    )

    badge_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    business_title = models.CharField(
        max_length=200,
        choices=FUNCTIONS,
        null=True,
        blank=True,
    )
    supervisor = models.IntegerField(default=0)
    terminated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()

# INDIVIDUAL TRACKER-

class Project_Name(models.Model):
    name = models.CharField(max_length=200)
    expired = models.BooleanField(default=False)
    full_name = models.CharField(max_length=200, null=False)
    badge_id = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Project_Time(models.Model):
    name = models.CharField(max_length=200)                         #name of the project
    description = models.TextField()
    who_approved_id = models.IntegerField(null=True)
    who_approved_name = models.CharField(max_length=200, null=True)
    super_stamp = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DateTimeField(null=True)
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Meeting_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DateTimeField(null=True)
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Training_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DateTimeField(null=True)
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()
