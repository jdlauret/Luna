import pytz
import datetime as dt
from datetime import date
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Auth_Employee, Project_Name, Project_Time, Meeting_Time, Training_Time

from P_Tracker.utilities.find_badge_id import find_badge_id
from P_Tracker.utilities.find_name import find_name
from P_Tracker.utilities.productivity_tracker import tracker_list

# todo create new users?
# todo supervisor or tl need to approve

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
        weekly_tracking = tracker_list(badge)
        date = dt.datetime.today().strftime('%m/%d/%y')
        today = dt.datetime.today()

        completed_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day)
        progress_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_projects = Project_Time.objects.all().filter(completed=False)

        completed_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day)
        progress_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_meetings = Meeting_Time.objects.all().filter(completed=False)

        completed_training = Training_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day)
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
                'project_progress':  progress_projects,
                'meeting_completed': completed_meeting,
                'meeting_progress': progress_meeting,
                'training_completed': completed_training,
                'training_progress': progress_training,
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
                'project_progress':  progress_projects,
                'meeting_completed': completed_meeting,
                'meeting_progress': progress_meeting,
                'training_completed': completed_training,
                'training_progress': progress_training,
                'hide_view': True,
            }
            return render(request, 'main.html', context)
    else:
        return HttpResponseRedirect('/Luna')

def input_project_time(request):
    email = request.user.email
    badge = find_badge_id(email)
    Project_Time.objects.proj_time_input(request.POST, badge)
    return redirect('/P_Tracker')

def end_project_time(request):
    for key, value in request.POST.items():
        project_time = Project_Time.objects.get(pk=int(value))
        project_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        project_time.completed = True
        project_time.total_time = project_time.end_time - project_time.start_time
        project_time.save()
    return redirect('/P_Tracker')

def input_meeting(request):
    email = request.user.email
    badge = find_badge_id(email)
    print(request.POST)
    Meeting_Time.objects.meeting_input(request.POST, badge)
    return redirect('/P_Tracker')

def end_meeting(request):
    for key, value in request.POST.items():
        meeting_time = Meeting_Time.objects.get(pk=int(value))
        meeting_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        meeting_time.completed = True
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
        training_time.save()
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
