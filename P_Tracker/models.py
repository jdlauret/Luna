from __future__ import unicode_literals
import datetime as dt
from django.db import models


class trackerManager(models.Manager):
    @classmethod
    def proj_time_input(self, post_data):
        errors = []
        badge_info = Auth_Employee.objects.get(badge_info=int(post_data['badge_id']))
        temp = Project_Time(
            name=post_data[''],
            description=post_data['description'],
            who_approved=post_data[''],
            start_time=post_data['start_time'],
            end_time=post_data['end_time'],
            auth_employee=post_data[''],
        )
        temp.save()

    @classmethod
    def proj_name_input(self, post_data):
        errors = []
        badge_info = Auth_Employee.objects.get(badge_info=int(post_data['badge_id']))
        temp = Project_Name(
            name=post_data[''],
            who_created=post_data[''],
            auth_employee=post_data[''],
        )
        temp.save()

    @classmethod
    def meeting_input(self, post_data):
        error = []
        badge_info = Auth_Employee.objects.get(badge_info=int(post_data['badge_id']))
        temp = Meeting_Time(
            name=post_data['name'],
            start_time=post_data[''],
            end_time=post_data[''],
            auth_employee=post_data[''],
        )
        temp.save()

    @classmethod
    def training_input(self, post_data):
        error = []
        badge_info = Auth_Employee.objects.get(badge_info=int(post_data['badge_id']))
        temp = Training_Time(
            name=post_data['name'],
            start_time=post_data[''],
            end_time=post_data[''],
            auth_employee=post_data[''],
        )
        temp.save()


# THIS ALLOWS PEOPLE ACcESS TO THE PRODUCTIVITY TRACKER
class Auth_Employee(models.Model):
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
    who_created = models.CharField(max_length=200)
    expired = models.BooleanField(default=False)
    business_title = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Project_Time(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    who_approved = models.CharField(max_length=200)
    super_stamp = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Meeting_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()


class Training_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = trackerManager()
