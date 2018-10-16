import pytz
import datetime as dt
import pandas as pd
import numpy as np
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil import parser
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from .models import Auth_Employee, Project_Name, Project_Time, Meeting_Time, Training_Time

from P_Tracker.utilities.find_badge_id import find_badge_id
from P_Tracker.utilities.find_name import find_name
from P_Tracker.utilities.productivity_tracker import tracker_list


# todo work on filter time
# todo prevent access to tracker from those who do not have access
# todo allow admin to access page but not show up as supervisor
# todo end project time, if agent forgets to end time, input 10 hours automatically, after 10 hours have passed
# todo rejection to projects box
# todo make supervisors aware of a project that is longer than 4 hrs
# todo if not approved, does not count in daily numbers
# todo edit project and input new project, create new tab
# todo see who edits the projects
# todo merge filter projects, meetings and trainings into one
# todo move need to approve to outside and set the filter to the person logged in

def email_check(user):
    return user.email.endswith('@vivintsolar.com')


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)

        weekly_tracking = tracker_list(badge)
        date = dt.datetime.today().strftime('%m/%d/%y')
        today = dt.datetime.today()

        # Shows Daily Tracker
        stat_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=True, end_time__year=today.year,
                                                    end_time__month=today.month, end_time__day=today.day,
                                                    super_stamp=None).aggregate(Sum('total_time'))['total_time__sum']
        stat_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=True, end_time__year=today.year,
                                                   end_time__month=today.month, end_time__day=today.day).aggregate(
            Sum('total_time'))['total_time__sum']
        stat_training = Training_Time.objects.filter(auth_employee_id=badge, completed=True, end_time__year=today.year,
                                                     end_time__month=today.month, end_time__day=today.day).aggregate(
            Sum('total_time'))['total_time__sum']

        # Filters the Project tab
        completed_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                         start_time__year=today.year, start_time__month=today.month,
                                                         start_time__day=today.day)
        progress_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_projects = Project_Time.objects.all().filter(completed=False)

        # Filters the Meeting Tab
        completed_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                        start_time__year=today.year, start_time__month=today.month,
                                                        start_time__day=today.day)
        progress_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_meetings = Meeting_Time.objects.all().filter(completed=False)

        # Filters the Training Tab
        completed_training = Training_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                          start_time__year=today.year, start_time__month=today.month,
                                                          start_time__day=today.day)
        progress_training = Training_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_training = Training_Time.objects.all().filter(completed=False)

        if len(find_completed_projects) > 0 or len(find_completed_meetings) > 0 or len(find_completed_training) > 0:
            context = {
                'name': name,
                'approved_by': Auth_Employee.objects.all().exclude(business_title='employee'),
                'project_name': Project_Name.objects.all().exclude(expired=True),
                'weekly_list': weekly_tracking,
                'today_date': date,
                'start_time': dt.datetime.now(),
                'end_time': dt.datetime.now(),
                'project_completed': completed_projects,
                'project_progress': progress_projects,
                'meeting_completed': completed_meeting,
                'meeting_progress': progress_meeting,
                'training_completed': completed_training,
                'training_progress': progress_training,
                'stat_projects': stat_projects,
                'stat_meeting': stat_meeting,
                'stat_training': stat_training,
                'hide_view': False,
            }
            return render(request, 'main.html', context)
        else:
            context = {
                'name': name,
                'approved_by': Auth_Employee.objects.all().exclude(business_title='employee'),
                'project_name': Project_Name.objects.all().exclude(expired=True),
                'weekly_list': weekly_tracking,
                'today_date': date,
                'start_time': dt.datetime.now(),
                'end_time': dt.datetime.now(),
                'project_completed': completed_projects,
                'project_progress': progress_projects,
                'meeting_completed': completed_meeting,
                'meeting_progress': progress_meeting,
                'training_completed': completed_training,
                'training_progress': progress_training,
                'stat_projects': stat_projects,
                'stat_meeting': stat_meeting,
                'stat_training': stat_training,
                'hide_view': True,
            }
            return render(request, 'main.html', context)
    else:
        return HttpResponseRedirect('/Luna')


def input_project_time(request):
    email = request.user.email
    badge = find_badge_id(email)
    results = Project_Time.objects.proj_time_input(request.POST, badge)
    if type(results) == list:
        for err in results:
            messages.error(request, err)
            return redirect('/P_Tracker')
    return redirect('/P_Tracker')


def end_project_time(request):
    for key, value in request.POST.items():
        project_time = Project_Time.objects.get(pk=int(value))
        project_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        project_time.completed = True

        total = project_time.end_time - project_time.start_time
        total = total / timedelta(hours=1)
        project_time.total_time = total

        project_time.save()
    return redirect('/P_Tracker')


def input_meeting(request):
    email = request.user.email
    badge = find_badge_id(email)
    Meeting_Time.objects.meeting_input(request.POST, badge)
    return redirect('/P_Tracker')


def end_meeting(request):
    for key, value in request.POST.items():
        meeting_time = Meeting_Time.objects.get(pk=int(value))
        meeting_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        meeting_time.completed = True

        total = meeting_time.end_time - meeting_time.start_time
        total = total / timedelta(hours=1)
        meeting_time.total_time = total

        meeting_time.save()
    return redirect('/P_Tracker')


def input_training(request):
    email = request.user.email
    badge = find_badge_id(email)
    Training_Time.objects.training_input(request.POST, badge)
    return redirect('/P_Tracker')


def end_training(request):
    for key, value in request.POST.items():
        training_time = Training_Time.objects.get(pk=int(value))
        training_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        training_time.completed = True

        total = training_time.end_time - training_time.start_time
        total = total / timedelta(hours=1)
        training_time.total_time = total

        training_time.save()
    return redirect('/P_Tracker')


@login_required
@user_passes_test(email_check)
def employee(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        today = dt.datetime.today()
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            for key, value in request.POST.items():
                try:
                    print('value', value)
                    weekly_tracking = tracker_list(int(value))
                    print('weekly', weekly_tracking)
                    single_employee = Auth_Employee.objects.get(badge_id=int(value))
                    need_approval = Project_Time.objects.filter(who_approved_id='104550',  # badge,
                                                                auth_employee_id=single_employee,
                                                                super_stamp='').order_by('created_at')
                    if len(value) > 0:
                        # Shows Daily Tracker
                        stat_projects = \
                            Project_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                        end_time__year=today.year,
                                                        end_time__month=today.month, end_time__day=today.day,
                                                        super_stamp=None).aggregate(Sum('total_time'))[
                                'total_time__sum']
                        stat_meeting = \
                            Meeting_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                        end_time__year=today.year,
                                                        end_time__month=today.month, end_time__day=today.day).aggregate(
                                Sum('total_time'))['total_time__sum']
                        stat_training = \
                            Training_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                         end_time__year=today.year,
                                                         end_time__month=today.month,
                                                         end_time__day=today.day).aggregate(
                                Sum('total_time'))['total_time__sum']

                        project_list = Project_Time.objects.filter(auth_employee_id=single_employee,
                                                                   end_time__year=today.year,
                                                                   end_time__month=today.month,
                                                                   end_time__day=today.day).order_by('created_at')
                        s_employee = Auth_Employee.objects.get(badge_id=single_employee.supervisor)
                        context = {
                            'name': name,
                            'all_names': Auth_Employee.objects.all(),
                            'employee_names': single_employee,
                            'employee_weekly': weekly_tracking,
                            'supervisor': s_employee,
                            'single_employee': single_employee,
                            'single_employee_super_name': Auth_Employee.objects.get(badge_id=s_employee.badge_id),
                            'stat_projects': stat_projects,
                            'stat_meeting': stat_meeting,
                            'stat_training': stat_training,
                            'need_approval': reversed(need_approval),
                            'project_list': reversed(project_list),
                            # 'super_stamp': False,
                            'super_badge': badge,
                            'list_super': Auth_Employee.objects.all().exclude(business_title='employee'),
                            'table': True,
                            'today': today,
                        }
                        return render(request, 'employee.html', context)
                    else:
                        # Shows Daily Tracker
                        stat_projects = Project_Time.objects.filter(auth_employee_id=single_employee, completed=True,
                                                                    end_time__year=today.year,
                                                                    end_time__month=today.month,
                                                                    end_time__day=today.day).aggregate(
                            Sum('total_time'))['total_time__sum']
                        stat_meeting = Meeting_Time.objects.filter(auth_employee_id=single_employee, completed=True,
                                                                   end_time__year=today.year,
                                                                   end_time__month=today.month,
                                                                   end_time__day=today.day).aggregate(
                            Sum('total_time'))['total_time__sum']
                        stat_training = Training_Time.objects.filter(auth_employee_id=single_employee, completed=True,
                                                                     end_time__year=today.year,
                                                                     end_time__month=today.month,
                                                                     end_time__day=today.day).aggregate(
                            Sum('total_time'))['total_time__sum']

                        project_list = Project_Time.objects.filter(auth_employee_id=single_employee,
                                                                   end_time__year=today.year,
                                                                   end_time__month=today.month,
                                                                   end_time__day=today.day).order_by('created_at')

                        context = {
                            'name': name,
                            'all_names': Auth_Employee.objects.all(),
                            'employee_names': single_employee,
                            'employee_weekly': weekly_tracking,
                            'supervisor': Auth_Employee.objects.get(badge_id=single_employee.supervisor),
                            'stat_projects': stat_projects,
                            'stat_meeting': stat_meeting,
                            'stat_training': stat_training,
                            'need_approval': reversed(need_approval),
                            'project_list': reversed(project_list),
                            # 'super_stamp': True,
                            'super_badge': badge,
                            'list_super': Auth_Employee.objects.all().exclude(business_title='employee'),
                            'table': False,
                            'today': today,
                        }
                        return render(request, 'employee.html', context)

                except Exception as e:
                    messages.error(request, e)
                    return redirect('/P_Tracker/employee')

            context = {
                'name': name,
                'all_names': Auth_Employee.objects.all(),
            }
            return render(request, 'employee.html', context)
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


def stamp_approval(request):
    results = Project_Time.objects.stamp_approval(request.POST)
    if type(results) == list:
        for err in results:
            messages.error(request, err)
            return redirect('/P_Tracker/employee')
    else:
        messages.success(request, 'Approval Accepted')
    return redirect('/P_Tracker/employee')


def edit_employee(request):
    results = Auth_Employee.objects.edit_status(request.POST)
    if type(results) == list:
        for err in results:
            messages.error(request, err)
            return redirect('/P_Tracker/employee')
    else:
        messages.success(request, 'Successfully edited Information')
    return redirect('/P_Tracker/employee')


@login_required
@user_passes_test(email_check)
def filter(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            results = Project_Time.objects.pull_filter_info(request.POST)
            start = parser.parse(results['start'])
            start = start.replace(tzinfo=pytz.timezone('US/Mountain'))
            end = parser.parse(results['end'])
            end = end.replace(hour=23, minute=59, second=59, tzinfo=pytz.timezone('US/Mountain'))

            # FILTER BETWEEN TWO TIMES, START AND END
            proj_time_given = Project_Time.objects.filter(start_time__gte=start, end_time__lte=end,
                                                     auth_employee_id=results['badge'])
            meeting_time_given = Meeting_Time.objects.filter(start_time__gte=start, end_time__lte=end,
                                                     auth_employee_id=results['badge'])
            training_time_given = Training_Time.objects.filter(start_time__gte=start, end_time__lte=end,
                                                     auth_employee_id=results['badge'])
            if type(results) == list:
                for err in results:
                    messages.error(request, err)
                    return redirect('/P_Tracker/employee')

            if results['name'] == 'Project':
                context = {
                    'name': name,
                    'filtered_by_name': results['name'],
                    'project_info': True,
                    'time_given': proj_time_given,
                }
                return render(request, 'filter.html', context)
            if results['name'] == 'Meeting':
                context = {
                    'name': name,
                    'filtered_by_name': results['name'],
                    'meeting_info': True,
                    'time_given': meeting_time_given,
                }
                return render(request, 'filter.html', context)
            if results['name'] == 'Training':
                context = {
                    'name': name,
                    'filtered_by_name': results['name'],
                    'training_info': True,
                    'time_given': training_time_given,
                }
                return render(request, 'filter.html', context)
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def create_project(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            project = Project_Name.objects.all().exclude(expired=True)
            context = {
                'name': name,
                'project_name': project,
            }
            return render(request, 'createProject.html', context)
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


def submit_project(request):
    email = request.user.email
    badge = find_badge_id(email)
    name = find_name(badge)
    Project_Name.objects.proj_name_input(request.POST, badge, name)
    return redirect('/P_Tracker/create_project')


def update_project(request):
    email = request.user.email
    badge = find_badge_id(email)
    name = find_name(badge)
    for key, value in request.POST.items():
        project = Project_Name.objects.get(pk=key)
        project.expired = True
        project.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        project.save()
    return redirect('/P_Tracker/create_project')


@login_required
@user_passes_test(email_check)
def create_new_user(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            return render(request, 'create_user.html')
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


def creation_of_user(request):
    Auth_Employee.objects.creation_of_new_user(request.POST)
    messages.success(request, 'Successfully Created a New User')
    return redirect('/P_Tracker/create_user')
