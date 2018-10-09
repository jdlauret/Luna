import pytz
import datetime as dt
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Auth_Employee, Project_Name, Project_Time, Meeting_Time, Training_Time

from P_Tracker.utilities.find_badge_id import find_badge_id
from P_Tracker.utilities.find_name import find_name
from P_Tracker.utilities.productivity_tracker import tracker_list


def email_check(user):
    return user.email.endswith('@vivintsolar.com')

# def tracker_access(user):
# 	return user.groups.filter(name='').exists()


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        weekly_tracking = tracker_list('205141')
        date = dt.datetime.today().strftime('%m/%d/%y')
        context = {
            'name': name,
            'approved_by': Auth_Employee.objects.all().exclude(business_title='employee'),
            'project_name': Project_Name.objects.all().exclude(expired=True),
            'weekly_list': weekly_tracking,
            'today_date': date,
            'start_time': dt.datetime.now(),
            'end_time': dt.datetime.now(),
        }
        return render(request, 'main.html', context)
    else:
        return HttpResponseRedirect('/Luna')

def input_project_time(request):
    email = request.user.email
    badge = find_badge_id(email)
    # Project_Time.objects.proj_time_input(request.Post, badge)
    print(request.POST)
    return redirect('/P_Tracker')


@login_required
@user_passes_test(email_check)
def employee(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        for key, value in request.POST.items():
            weekly_tracking = tracker_list(value)
            single_employee = Auth_Employee.objects.get(badge_id=value)
            context = {
                'name': name,
                'all_names': Auth_Employee.objects.all(),
                'employee_names': single_employee,
                'employee_weekly': weekly_tracking,
                'supervisor': Auth_Employee.objects.get(badge_id=single_employee.supervisor),
                # TODO work on getting all projects
                # 'all_working_projects': Project_Time.objects.get(auth_employee=value).order_by('created_at'),
            }
            return render(request, 'employee.html', context)
        context = {
            'name': name,
            'all_names': Auth_Employee.objects.all(),
        }
        return render(request, 'employee.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def create_project(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        project = Project_Name.objects.all().exclude(expired=True)
        context = {
            'name': name,
            'project_name': project,
        }
        return render(request, 'createProject.html', context)
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
