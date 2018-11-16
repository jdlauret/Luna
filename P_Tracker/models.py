from __future__ import unicode_literals
from datetime import datetime as dt, timedelta
import pytz
from django.db import models
from dateutil import parser


class trackerManager(models.Manager):
    @classmethod
    def proj_time_input(self, post_data, badge_id):
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
        if len(post_data) < 0 or len(badge) < 0:
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
        if len(post_data) < 0 or len(badge_id) < 0:
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
        if len(post_data) < 0 or len(badge_id) < 0:
            errors.append('No information was entered, please try again')
            return errors
        else:
            temp = Training_Time(
                name=post_data['training_name'],
                start_time=dt.now(pytz.timezone('US/Mountain')),
                auth_employee_id=badge_id,
            )
            temp.save()

    @classmethod
    def creation_of_new_user(self, post_data):
        errors = []
        if len(post_data) <= 0:
            errors.append('No information was entered, please try again')
            return errors
        else:
            temp = Auth_Employee(
                badge_id=int(post_data['badge_id']),
                full_name=post_data['full_name'],
                business_title=post_data['business_title'],
                supervisor=int(post_data['supervisor_id']),
                created_at=dt.now(pytz.timezone('US/Mountain')),
                edited_at=dt.now(pytz.timezone('US/Mountain')),
            )
            temp.save()

    @classmethod
    def stamp_approval(self, post_data):
        errors = []
        if len(post_data['id']) == 0:
            errors.append('No information was checked')
            return errors
        else:
            accept_reject = post_data.getlist('accept_reject')
            accept_id = post_data.getlist('id')
            if post_data['type'] == 'project':
                for x in range(len(accept_id)):
                    project = Project_Time.objects.get(id=accept_id[x])
                    project.super_stamp = post_data['stamp']
                    if accept_reject[x] == 'reject':
                        project.accept = False
                        project.save()
                    else:
                        project.accept = True
                        project.save()
            elif post_data['type'] == 'meeting':
                for y in range(len(accept_id)):
                    meeting = Meeting_Time.objects.get(id=accept_id[y])
                    meeting.super_stamp = post_data['stamp']
                    if accept_reject[y] == 'reject':
                        meeting.accept = False
                        meeting.save()
                    else:
                        meeting.accept = True
                        meeting.save()
            else:
                for z in range(len(accept_id)):
                    training = Training_Time.objects.get(id=accept_id[z])
                    training.super_stamp = post_data['stamp']
                    if accept_reject[z] == 'reject':
                        training.accept = False
                        training.save()
                    else:
                        training.accept = True
                        training.save()

    @classmethod
    def edit_status(self, post_data):
        errors = []
        if post_data['supervisor'] == 'null' and post_data['business_title'] == 'null':
            errors.append('No information was selected')
            return errors
        elif post_data['supervisor'] == 'null' and len(post_data['business_title']) > 0:
            employee = Auth_Employee.objects.get(badge_id=post_data['badge_id'])
            employee.business_title = post_data['business_title']
            employee.save()

        elif post_data['business_title'] == 'null' and len(post_data['supervisor']) > 0:
            employee = Auth_Employee.objects.get(badge_id=post_data['badge_id'])
            employee.supervisor = post_data['supervisor']
            employee.save()

        else:
            employee = Auth_Employee.objects.get(badge_id=post_data['badge_id'])
            employee.supervisor = post_data['supervisor']
            employee.business_title = post_data['business_title']
            employee.save()

    @classmethod
    def pull_filter_info(self, post_data):
        errors = []
        info = {}
        if len(post_data['start']) == 0 or len(post_data['end']) == 0:
            errors.append('No information was selected')
            return errors
        else:
            info['name'] = post_data['what_to_filter']
            info['start'] = post_data['start']
            info['end'] = post_data['end']
            info['badge'] = post_data['badge_id']
            return info

    @classmethod
    def manual_input(self, post_data):
        errors = []
        tz = pytz.timezone('US/Mountain')
        if len(post_data['start_time']) == 0 or len(post_data['end_time']) == 0:
            errors.append('No information was selected')
            return errors
        else:
            if post_data['type'] == 'project':
                end = post_data['end_time']
                end = parser.parse(end)
                end = end.replace(tzinfo=tz)
                start = post_data['start_time']
                start = parser.parse(start)
                start = start.replace(tzinfo=tz)
                if start > end:
                    errors.append('Start Time needs to be less than End Time')
                    return errors
                else:
                    total = end-start
                    total = total / timedelta(hours=1)
                    pn = int(post_data['project_name'])
                    name = Project_Name.objects.get(id=pn)
                    who_approved = Auth_Employee.objects.get(badge_id=int(post_data['approved_by']))

                    temp = Project_Time(
                        name=name.name,
                        description=post_data['description'],
                        who_approved_id=post_data['approved_by'],
                        who_approved_name=who_approved.full_name,
                        start_time=start,
                        end_time=end,
                        total_time=total,
                        completed=True,
                        auth_employee_id=post_data['badge_id'],
                        edited_at=dt.now(pytz.timezone('US/Mountain')),
                        who_edited=post_data['super_badge'],
                        accept=True,
                        super_stamp=post_data['super_badge'],
                    )
                    temp.save()
            elif post_data['type'] == 'meeting':
                end = post_data['end_time']
                end = parser.parse(end)
                end = end.replace(tzinfo=tz)
                start = post_data['start_time']
                start = parser.parse(start)
                start = start.replace(tzinfo=tz)
                if start > end:
                    errors.append('Start Time needs to be less than End Time')
                    return errors
                else:
                    total = end - start
                    total = total / timedelta(hours=1)

                    temp_m = Meeting_Time(
                        name=post_data['name'],
                        start_time=start,
                        end_time=end,
                        total_time=total,
                        completed=True,
                        auth_employee_id=post_data['badge_id'],
                        edited_at=dt.now(pytz.timezone('US/Mountain')),
                        who_edited=post_data['super_badge'],
                        accept=True,
                        super_stamp=post_data['super_badge']
                    )
                    temp_m.save()
            else:
                end = post_data['end_time']
                end = parser.parse(end)
                end = end.replace(tzinfo=tz)
                start = post_data['start_time']
                start = parser.parse(start)
                start = start.replace(tzinfo=tz)
                if start > end:
                    errors.append('Start Time needs to be less than End Time')
                    return errors
                else:
                    total = end - start
                    total = total / timedelta(hours=1)

                    temp_t = Training_Time(
                        name=post_data['name'],
                        start_time=start,
                        end_time=end,
                        total_time=total,
                        completed=True,
                        auth_employee_id=post_data['badge_id'],
                        edited_at=dt.now(pytz.timezone('US/Mountain')),
                        who_edited=post_data['super_badge'],
                        accept=True,
                        super_stamp=post_data['super_badge']
                    )
                    temp_t.save()

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
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)  # name of the project
    description = models.TextField()
    who_approved_id = models.IntegerField(null=True)
    who_approved_name = models.CharField(max_length=200, null=True)
    super_stamp = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    who_edited = models.IntegerField(null=True)
    edited_at = models.DateTimeField(null=True)
    accept = models.BooleanField(default=False)
    objects = trackerManager()


class Meeting_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    who_edited = models.IntegerField(null=True)
    edited_at = models.DateTimeField(null=True)
    accept = models.BooleanField(default=False)
    super_stamp = models.CharField(max_length=200, null=True)
    objects = trackerManager()


class Training_Time(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    total_time = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    auth_employee = models.ForeignKey('Auth_Employee', on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    who_edited = models.IntegerField(null=True)
    edited_at = models.DateTimeField(null=True)
    accept = models.BooleanField(default=False)
    super_stamp = models.CharField(max_length=200, null=True)
    objects = trackerManager()
