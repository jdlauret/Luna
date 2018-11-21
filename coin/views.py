from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import employee_id, transaction
from .utilities.user_list import user_list
from coin.utilities import find_badge_id
from coin.utilities.create_new_user import new_user
from coin.utilities.change_status_termination import terminated_user

# TODO SEND EMAILS -> NOTIFICATION SYSTEM
# TODO AUTOMATOR TO UPLOAD TRANSACTION HISTORY
# TODO ONLY ACCESS CERTAIN PARTS OF THE SITE FOR CERTAIN PEOPLE
# TODO SUBMIT PICTURES WHAT THEY WANT IN THE STORE
# idea generator:
# submit pictures of what they would like in the store
# votes?
# TODO Community Like button


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


def overlord_access(user):
    return user.groups.filter(name='Coin_Overlord').exists()


def create_new_user_button(request):
    result = new_user()
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/overlord_view')
    messages.success(request, 'Created new users')
    return redirect('/coin/overlord_view')


def terminated_user_button(request):
    result = terminated_user()
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/overlord_view')
    messages.success(request, 'Removed Terminated Users')
    return redirect('/coin/overlord_view')


# GLOBAL SECTION
@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        try:
            email = request.user.email
            badge_id = find_badge_id(email)
            agent = employee_id.objects.get(badgeid=badge_id)
            t1 = transaction.objects.all().order_by('created_at').reverse()
            paginator = Paginator(t1, 15)
            page = request.GET.get('page')
            transaction_list = paginator.get_page(page)
            context = {
                'transaction': transaction_list,
                'coin': agent.allotment,
            }
            return render(request, 'global.html', context)
        except Exception as e:
            messages.error(request, 'Creating New User')
            new_user()
            return redirect('/coin/global')
    else:
        return HttpResponseRedirect('/Luna')

# AGENT SECTION
@login_required
@user_passes_test(email_check)
def agent(request):
    if request.user.is_authenticated:
        try:
            email = request.user.email
            badge_id = find_badge_id(email)
            agent = employee_id.objects.get(badgeid=badge_id)
            a1 = transaction.objects.filter(benefactor=badge_id).order_by('created_at')
            a2 = transaction.objects.filter(recipient=badge_id).order_by('created_at')
            # print(transaction.objects.filter((benefactor=badge_id) or (recipient=badge_id)))
            context = {
                'allt1': a1.reverse()[:25],  # View All
                'allt2': a2.reverse()[:25],  # View All

                'senttransaction': a2.reverse()[:50],  # View Sent
                'fromtransaction': a1.reverse()[:50],  # View received
                'employee_id': employee_id.objects.all,
                'coin': agent.allotment,
                'badge_id': badge_id,
            }
            return render(request, 'agent_view.html', context)
        except Exception as e:
            messages.error(request, 'Creating New User')
            new_user()
            return redirect('/coin/agent')
    else:
        return HttpResponseRedirect('/Luna')

# TRANSACTION SECTION
@login_required
@user_passes_test(email_check)
def transactions(request):
    if request.user.is_authenticated:
        try:
            email = request.user.email
            badge_id = find_badge_id(email)
            agent = employee_id.objects.get(badgeid=badge_id)
            context = {
                'badge_id': badge_id,
                'user_list': user_list(),
                'coin': agent.allotment,
            }
            return render(request, 'transaction_window.html', context)
        except Exception as e:
            messages.error(request, 'Creating New User')
            new_user()
            return redirect('/coin/transaction')
    else:
        return HttpResponseRedirect('/Luna')


# VALIDATES THE TRANSACTION THAT IS SUBMITTED
def submit_transaction(request):
    result = transaction.objects.validate_transaction(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/transaction')
    messages.success(request, 'Success')
    return redirect('/coin/transaction')


# OVERLORD MAIN PAGE
@login_required
@user_passes_test(overlord_access)
def overlord_view(request):
    if request.user.is_authenticated:
        context = {
            'transaction': reversed(transaction.objects.all().order_by('created_at')),
            'employee': employee_id.objects.filter(terminated=0).order_by('name'),
        }
        return render(request, 'overlord_view.html', context)
    else:
        return HttpResponseRedirect('/Luna')


# OVERLORD CONTROL PANEL
@login_required
@user_passes_test(overlord_access)
def control_panel(request):
    if request.user.is_authenticated:
        info_request = request.POST.getlist('badge_id')
        for i, value in enumerate(info_request):
            requested = int(value)
            try:
                context = {
                    'employee_info': employee_id.objects.get(badgeid=requested),
                    'employee_history': reversed(
                        transaction.objects.filter(benefactor=requested).order_by('created_at')),
                    'user_list': user_list(),
                }
            except Exception as e:
                context = {
                    'employee_info': employee_id.objects.get(badgeid=requested),
                }
            return render(request, 'overlord_control_panel.html', context)
    else:
        return HttpResponseRedirect('/Luna')

# CREATES A TRANSACTION FROM OVERLORD
def overlord_create_trans(request):
    result = employee_id.objects.ol_transaction(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/overlord_view')
    messages.success(request, 'Success')
    return redirect('/coin/overlord_view')

# EDIT THE EMPLOYEE ALLOTMENT: CHANGES HOW MUCH YOU CAN GIVE TO THE EMPLOYEE
def employee_load(request):
    result = employee_id.objects.employee_action(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/overlord_view')
    messages.success(request, 'Success')
    return redirect('/coin/overlord_view')

# EDIT THE TRANSACTION HISTORY: MONITOR BAD COMMENTS
def trans_load(request):
    id_list = request.POST.getlist('id')
    bad_list = request.POST.getlist('bad_comment')
    for i, value in enumerate(id_list):
        trans = transaction.objects.get(id=value)
        trans.bad_comment = bad_list[i]
        trans.save()
    messages.success(request, 'Success')
    return redirect('/coin/overlord_view')
