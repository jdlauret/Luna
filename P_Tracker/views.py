import pytz
import datetime as dt
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


# todo prevent access to tracker from those who do not have access?

# TRACKER VERSION 2:
# todo make supervisors aware of a project that is longer than 4 hrs
# todo need to set the select name to current name

def email_check(user):
    return user.email.endswith('@vivintsolar.com')


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        tz = pytz.timezone('US/Mountain')
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        weekly_tracking = tracker_list(badge)
        # if weekly_tracking == 'error':
        date = dt.datetime.today().strftime('%m/%d/%y')
        today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
        first_date = today - timedelta(days=today.weekday())
        last_date = first_date + timedelta(days=5)
        last_date = last_date.replace(hour=23, minute=59, second=59, tzinfo=pytz.timezone('US/Mountain'))

        # Shows Daily Tracker
        stat_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__gte=first_date,
                                                    end_time__lte=last_date, accept=True).aggregate(Sum('total_time'))[
            'total_time__sum']
        stat_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__gte=first_date,
                                                   end_time__lte=last_date, accept=True).aggregate(Sum('total_time'))[
            'total_time__sum']
        stat_training = Training_Time.objects.filter(auth_employee_id=badge, completed=True, start_time__gte=first_date,
                                                     end_time__lte=last_date, accept=True).aggregate(Sum('total_time'))[
            'total_time__sum']

        # Filters the Project tab
        completed_projects = Project_Time.objects.reverse().filter(auth_employee_id=badge, completed=True,
                                                                   start_time__gte=first_date,
                                                                   end_time__lte=last_date).order_by('start_time')
        progress_projects = Project_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_projects = Project_Time.objects.filter(completed=False, auth_employee=badge)

        # Filters the Meeting Tab
        completed_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                        start_time__gte=first_date, end_time__lte=last_date).order_by(
            'start_time')
        progress_meeting = Meeting_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_meetings = Meeting_Time.objects.filter(completed=False, auth_employee=badge)

        # Filters the Training Tab
        completed_training = Training_Time.objects.filter(auth_employee_id=badge, completed=True,
                                                          start_time__gte=first_date, end_time__lte=last_date).order_by(
            'start_time')
        progress_training = Training_Time.objects.filter(auth_employee_id=badge, completed=False)
        find_completed_training = Training_Time.objects.filter(completed=False, auth_employee=badge)
        uncompleted_projects = Project_Time.objects.filter(completed=False)

        # UNCOMPLETED PROJECTS
        for x in uncompleted_projects:
            check = int((dt.datetime.now(pytz.timezone('US/Mountain')) - x.start_time).seconds / 60 / 60)
            if check >= 10:
                x.end_time = x.start_time + timedelta(hours=10)
                total = x.end_time - x.start_time
                total = total / timedelta(hours=1)
                x.total_time = total
                x.completed = True
                x.save()
        uncompleted_meeting = Meeting_Time.objects.all().filter(completed=False)

        # UNCOMPLETED MEETING
        for y in uncompleted_meeting:
            check = int((dt.datetime.now(pytz.timezone('US/Mountain')) - y.start_time).seconds / 60 / 60)
            if check >= 10:
                y.end_time = y.start_time + timedelta(hours=10)
                total = y.end_time - y.start_time
                total = total / timedelta(hours=1)
                y.total_time = total
                y.completed = True
                y.save()
        uncompleted_training = Training_Time.objects.all().filter(completed=False)

        # UNCOMPLETED TRAINING
        for z in uncompleted_training:
            check = int((dt.datetime.now(pytz.timezone('US/Mountain')) - z.start_time).seconds / 60 / 60)
            if check >= 10:
                z.end_time = z.start_time + timedelta(hours=10)
                total = z.end_time - z.start_time
                total = total / timedelta(hours=1)
                z.total_time = total
                z.completed = True
                z.save()

        if len(find_completed_projects) > 0 or len(find_completed_meetings) > 0 or len(find_completed_training) > 0:
            context = {
                'name': name,
                'approved_by': Auth_Employee.objects.exclude(business_title='employee', terminated=False).exclude(
                    business_title='admin').exclude(business_title='tl').exclude(badge_id=badge),
                'project_name': Project_Name.objects.all().exclude(expired=True),
                'weekly_list': weekly_tracking,
                'today_date': date,
                'first_date': first_date.strftime('%m/%d/%y'),
                'start_time': dt.datetime.now(pytz.timezone('US/Mountain')),
                'end_time': dt.datetime.now(pytz.timezone('US/Mountain')),
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
                'approved_by': Auth_Employee.objects.exclude(business_title='employee', terminated=False).exclude(
                    business_title='admin').exclude(business_title='tl').exclude(badge_id=badge),
                'project_name': Project_Name.objects.all().exclude(expired=True),
                'weekly_list': weekly_tracking,
                'today_date': date,
                'first_date': first_date.strftime('%m/%d/%y'),
                'start_time': dt.datetime.now(pytz.timezone('US/Mountain')),
                'end_time': dt.datetime.now(pytz.timezone('US/Mountain')),
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
    return redirect('/P_Tracker/#meeting')


def end_meeting(request):
    for key, value in request.POST.items():
        meeting_time = Meeting_Time.objects.get(pk=int(value))
        meeting_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        meeting_time.completed = True

        total = meeting_time.end_time - meeting_time.start_time
        total = total / timedelta(hours=1)
        meeting_time.total_time = total

        meeting_time.save()
    return redirect('/P_Tracker/#meeting')


def input_training(request):
    email = request.user.email
    badge = find_badge_id(email)
    Training_Time.objects.training_input(request.POST, badge)
    return redirect('/P_Tracker/#training')


def end_training(request):
    for key, value in request.POST.items():
        training_time = Training_Time.objects.get(pk=int(value))
        training_time.end_time = dt.datetime.now(pytz.timezone('US/Mountain'))
        training_time.completed = True

        total = training_time.end_time - training_time.start_time
        total = total / timedelta(hours=1)
        training_time.total_time = total

        training_time.save()
    return redirect('/P_Tracker/#training')


@login_required
@user_passes_test(email_check)
def employee(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        tz = pytz.timezone('US/Mountain')
        today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
        first_date = today - timedelta(days=today.weekday())
        last_date = first_date + timedelta(days=5)
        last_date = last_date.replace(hour=23, minute=59, second=59, tzinfo=pytz.timezone('US/Mountain'))
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            if access.business_title != 'tl':
                try:
                    employee_badge = int(request.POST['employee_badge'])
                    weekly_tracking = tracker_list(employee_badge)
                    selected_employee = Auth_Employee.objects.get(badge_id=employee_badge)
                    need_approval = Project_Time.objects.reverse().filter(super_stamp='',
                                                                          auth_employee_id=selected_employee.badge_id,
                                                                          who_approved_id=badge)
                    need_approval_meeting = Meeting_Time.objects.reverse().filter(
                        auth_employee=selected_employee, super_stamp=None)
                    need_approval_training = Training_Time.objects.reverse().filter(
                        auth_employee=selected_employee, super_stamp=None)

                    if len(request.POST) > 0:
                        # Shows Daily Tracker
                        stat_projects = Project_Time.objects.filter(auth_employee_id=selected_employee, completed=True,
                                                                    start_time__gte=first_date, end_time__lte=last_date,
                                                                    accept=True).aggregate(Sum('total_time'))[
                            'total_time__sum']
                        stat_meeting = Meeting_Time.objects.filter(auth_employee_id=selected_employee, completed=True,
                                                                   start_time__gte=first_date, end_time__lte=last_date,
                                                                   accept=True).aggregate(Sum('total_time'))[
                            'total_time__sum']
                        stat_training = Training_Time.objects.filter(auth_employee_id=selected_employee, completed=True,
                                                                     start_time__gte=first_date,
                                                                     end_time__lte=last_date,
                                                                     accept=True).aggregate(Sum('total_time'))[
                            'total_time__sum']

                        project_list = Project_Time.objects.reverse().filter(auth_employee_id=selected_employee,
                                                                             start_time__gte=first_date,
                                                                             end_time__lte=last_date).order_by(
                            'created_at')
                        meeting_list = Meeting_Time.objects.reverse().filter(auth_employee_id=selected_employee,
                                                                             start_time__gte=first_date,
                                                                             end_time__lte=last_date).order_by(
                            'created_at')
                        training_list = Training_Time.objects.reverse().filter(auth_employee_id=selected_employee,
                                                                               start_time__gte=first_date,
                                                                               end_time__lte=last_date).order_by(
                            'created_at')

                        s_employee = Auth_Employee.objects.get(badge_id=selected_employee.supervisor)

                        context = {
                            'name': name,
                            'badge': badge,
                            'approved_by': Auth_Employee.objects.all().exclude(business_title='employee').exclude(
                                business_title='admin').exclude(business_title='tl').exclude(terminated=True),
                            'project_name': Project_Name.objects.filter(expired=False),
                            'all_names': Auth_Employee.objects.all().exclude(business_title='admin').exclude(
                                business_title='manager').exclude(terminated=True),
                            'employee_names': selected_employee,
                            'employee_weekly': weekly_tracking,
                            'supervisor': s_employee,
                            'selected_employee': selected_employee,
                            'selected_employee_supervisor': selected_employee.supervisor,
                            'single_employee_super_name': Auth_Employee.objects.get(badge_id=s_employee.badge_id),

                            'stat_projects': stat_projects,
                            'stat_meeting': stat_meeting,
                            'stat_training': stat_training,

                            'need_approval': need_approval,
                            'need_approval_meeting': need_approval_meeting,
                            'need_approval_training': need_approval_training,

                            'project_list': project_list,
                            'meeting_list': meeting_list,
                            'training_list': training_list,

                            'super_stamp': False,
                            'super_badge': badge,
                            'list_super': Auth_Employee.objects.all().exclude(business_title='employee').exclude(
                                business_title='admin').exclude(business_title='tl').exclude(terminated=True),
                            'table': True,
                            'today': today,
                        }
                        return render(request, 'employee.html', context)
                    else:
                        return redirect('/P_Tracker/employee')

                except Exception as e:
                    context = {
                        'name': name,
                        'all_names': Auth_Employee.objects.all().exclude(business_title='admin').exclude(
                            business_title='manager').exclude(terminated=True),
                    }
                    return render(request, 'employee.html', context)
            else:
                return redirect('/P_Tracker')
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def create_new_user(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            if access.business_title != 'tl':
                return render(request, 'create_user.html')
            else:
                return redirect('/P_Tracker')
        else:
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


def creation_of_user(request):
    Auth_Employee.objects.creation_of_new_user(request.POST)
    messages.success(request, 'Successfully Created a New User')
    return redirect('/P_Tracker/create_user')


def stamp_approval(request):
    if request.POST['type'] == 'project':
        results = Project_Time.objects.stamp_approval(request.POST)
        if type(results) == list:
            for err in results:
                messages.error(request, err)
                return redirect('/P_Tracker/employee')
        else:
            messages.success(request, 'Approval Accepted')
    elif request.POST['type'] == 'meeting':
        results = Meeting_Time.objects.stamp_approval(request.POST)
        if type(results) == list:
            for err in results:
                messages.error(request, err)
                return redirect('/P_Tracker/employee')
        else:
            messages.success(request, 'Approval Accepted')
    else:
        results = Training_Time.objects.stamp_approval(request.POST)
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


def manually_input_time(request):
    if request.POST['type'] == 'project':
        results = Project_Time.objects.manual_input(request.POST)
        if type(results) == list:
            for err in results:
                messages.error(request, err)
                return redirect('/P_Tracker/employee')
        else:
            messages.success(request, 'Success')
    if request.POST['type'] == 'meeting':
        results = Meeting_Time.objects.manual_input(request.POST)
        if type(results) == list:
            for err in results:
                messages.error(request, err)
                return redirect('/P_Tracker/employee')
        else:
            messages.success(request, 'Success')
    if request.POST['type'] == 'training':
        results = Training_Time.objects.manual_input(request.POST)
        if type(results) == list:
            for err in results:
                messages.error(request, err)
                return redirect('/P_Tracker/employee')
        else:
            messages.success(request, 'Success')
    return redirect('/P_Tracker/employee')


@login_required
@user_passes_test(email_check)
def filter_name(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge = find_badge_id(email)
        name = find_name(badge)
        access = Auth_Employee.objects.get(badge_id=badge)
        if access.business_title != 'employee':
            if access.business_title != 'tl':
                results = Project_Time.objects.pull_filter_info(request.POST)
                start = parser.parse(results['start'])
                start = start.replace(tzinfo=pytz.timezone('US/Mountain'))
                end = parser.parse(results['end'])
                end = end.replace(hour=23, minute=59, second=59, tzinfo=pytz.timezone('US/Mountain'))

                # FILTER BETWEEN TWO TIMES, START AND END
                proj_time_given = Project_Time.objects.filter(start_time__gte=start, end_time__lte=end,
                                                              auth_employee_id=int(results['badge']))
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
                        'project_names': Project_Name.objects.all(),
                        'super_list': Auth_Employee.objects.all().exclude(business_title='employee').exclude(
                            business_title='admin').exclude(terminated=True),
                        'stamp': badge,
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
            return redirect('/P_Tracker')
    else:
        return HttpResponseRedirect('/Luna')


def edit_project(request):
    email = request.user.email
    badge = find_badge_id(email)
    start_time = request.POST['start_time']
    start_time = parser.parse(start_time)
    start_time = start_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    end_time = request.POST['end_time']
    end_time = parser.parse(end_time)
    end_time = end_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    project = Project_Time.objects.get(id=int(request.POST['id']))
    accept = request.POST['accept']
    who_approved_name = Auth_Employee.objects.get(badge_id=request.POST['who_approved_by'])
    total = end_time - start_time
    total = total / timedelta(hours=1)

    if accept == 'True':
        project.name = request.POST['project_name']
        project.description = request.POST['description']
        project.who_approved_id = request.POST['who_approved_by']
        project.who_approved_name = who_approved_name.full_name
        project.start_time = start_time
        project.end_time = end_time
        project.total_time = total
        project.completed = True
        project.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        project.who_edited = badge
        project.accept = True
        project.save()
    else:
        project.name = request.POST['project_name']
        project.description = request.POST['description']
        project.who_approved_id = request.POST['who_approved_by']
        project.who_approved_name = who_approved_name.full_name
        project.start_time = start_time
        project.end_time = end_time
        project.total_time = total
        project.completed = True
        project.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        project.who_edited = badge
        project.accept = False
        project.save()
    return redirect('/P_Tracker/employee')


def edit_meeting(request):
    email = request.user.email
    badge = find_badge_id(email)
    start_time = request.POST['start_time']
    start_time = parser.parse(start_time)
    start_time = start_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    end_time = request.POST['end_time']
    end_time = parser.parse(end_time)
    end_time = end_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    total = end_time - start_time
    total = total / timedelta(hours=1)
    meeting = Meeting_Time.objects.get(id=int(request.POST['id']))
    accept = request.POST['accept']
    if accept == 'True':
        meeting.name = request.POST['name']
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.total_time = total
        meeting.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        meeting.who_edited = badge
        meeting.accept = True
        meeting.save()
    else:
        meeting.name = request.POST['name']
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.total_time = total
        meeting.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        meeting.who_edited = badge
        meeting.accept = False
        meeting.save()
    return redirect('/P_Tracker/employee')


def edit_training(request):
    email = request.user.email
    badge = find_badge_id(email)
    start_time = request.POST['start_time']
    start_time = parser.parse(start_time)
    start_time = start_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    end_time = request.POST['end_time']
    end_time = parser.parse(end_time)
    end_time = end_time.replace(tzinfo=pytz.timezone('US/Mountain'))
    total = end_time - start_time
    total = total / timedelta(hours=1)
    training = Training_Time.objects.get(id=int(request.POST['id']))
    accept = request.POST['accept']
    if accept == 'True':
        training.name = request.POST['name']
        training.start_time = start_time
        training.end_time = end_time
        training.total_time = total
        training.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        training.who_edited = badge
        training.accept = True
        training.save()
    else:
        training.name = request.POST['name']
        training.start_time = start_time
        training.end_time = end_time
        training.total_time = total
        training.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        training.who_edited = badge
        training.accept = False
        training.save()
    return redirect('/P_Tracker/employee')


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
    for key, value in request.POST.items():
        project = Project_Name.objects.get(pk=key)
        project.expired = True
        project.edited_at = dt.datetime.now(pytz.timezone('US/Mountain'))
        project.save()
    return redirect('/P_Tracker/create_project')
