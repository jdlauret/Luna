from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
import datetime as dt
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
        context = {
            'name': name,
            'approved_by': Auth_Employee.objects.all().exclude(business_title='employee'),
            'project_name': Project_Name.objects.all().exclude(expired=True),
            'weekly_list': weekly_tracking,
            'today_date': dt.datetime.now()
        }
        return render(request, 'main.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def employee(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        weekly_tracking = tracker_list(request.POST)

        # get_badge = find_badge_id(request)
        context = {
            'name': name,
            'employee_names': Auth_Employee.objects.all(),
            'employee_weekly': weekly_tracking,
        }
        return render(request, 'employee.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def createProject(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        context = {
            'name': name,
            'project_name': Project_Name.objects.all().exclude(expired=True),
        }
        return render(request, 'createProject.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def createEmployee(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        context = {
            'name': name,
        }
        return render(request, 'createEmployee.html', context)
    else:
        return HttpResponseRedirect('/Luna')
