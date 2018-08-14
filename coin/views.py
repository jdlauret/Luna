from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import employee_id, transaction
from .utilities.user_list import user_list
from coin.utilities import find_badge_id

def email_check(user):
    return user.email.endswith('@vivintsolar.com')

def overlord_access(user):
    return user.groups.filter(name='Coin_Overlord').exists()

@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge_id = find_badge_id(email)
        # employee_id.objects.create_user(request.POST)
        agent = employee_id.objects.get(badgeid=badge_id)
        context = {
            'transaction': reversed(transaction.objects.all().order_by('created_at')[:50]),
            'coin': agent.allotment,
        }
        return render(request, 'global.html', context)
    else:
        return HttpResponseRedirect('/Luna')

@login_required
@user_passes_test(email_check)
def agent(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge_id = find_badge_id(email)
        agent = employee_id.objects.get(badgeid=badge_id)
        a1 = transaction.objects.filter(benefactor=badge_id)
        a2 = transaction.objects.filter(recipient=badge_id)
        # print(transaction.objects.filter((benefactor=badge_id) or (recipient=badge_id)))
        context = {
            'allt1': reversed(a1.order_by('created_at')[:25]), #View All
            'allt2': reversed(a2.order_by('created_at')[:25]), #View All

            'senttransaction': reversed(a2.order_by('created_at')[:50]), #View Sent
            'fromtransaction': reversed(a1.order_by('created_at')[:50]), #View received
            # 'need_to_accept': reversed(
            #     transaction.objects.filter(recipient=badge_id).filter(need_to_accept=0).filter(rejected=0).order_by(
            #         'created_at')[:50]), #View Accepted Coin
            'employee_id': employee_id.objects.all,
            'coin': agent.allotment,
            'badge_id': badge_id,
        }
        return render(request, 'agent_view.html', context)
    else:
        return HttpResponseRedirect('/Luna')

@login_required
@user_passes_test(email_check)
def transactions(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge_id = find_badge_id(email)
        agent = employee_id.objects.get(badgeid=badge_id)
        context = {
            'badge_id': badge_id,
            'user_list': user_list(),
            'coin': agent.allotment,
        }
        return render(request, 'transaction_window.html', context)


def submit_transaction(request):
    result = transaction.objects.validate_transaction(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/transaction')
    messages.success(request, 'Success')
    return redirect('/coin/transaction')

# permission view
@login_required
@user_passes_test(overlord_access)
def overlord_view(request):
    if request.user.is_authenticated:
        context = {
            'transaction': reversed(transaction.objects.all().order_by('created_at')),
            'employee': employee_id.objects.all().order_by('name'),
        }
        return render(request, 'overlord_view.html', context)
    else:
        return HttpResponseRedirect('/Luna')

# permission view
@login_required
@user_passes_test(overlord_access)
def control_panel(request):
    if request.user.is_authenticated:
        info_request = request.POST.getlist('badge_id')
        for i, value in enumerate(info_request):
            requested = int(value)
            try:
                context={
                    'employee_info' : employee_id.objects.get(badgeid=requested),
                    'employee_history': reversed(transaction.objects.filter(benefactor=requested).order_by('created_at')),
                }
            except Exception as e:
                context={
                    'employee_info': employee_id.objects.get(badgeid=requested),
                }
            return render(request, 'overlord_control_panel.html', context)
    else:
        return HttpResponseRedirect('/Luna')

def employee_load(request):
    result = employee_id.objects.employee_action(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin/overlord_view')
    messages.success(request, 'Success')
    return redirect('/coin/overlord_view')

def trans_load(request):
    id_list = request.POST.getlist('id')
    bad_list = request.POST.getlist('bad_comment')
    for i, value in enumerate(id_list):
        trans = transaction.objects.get(id=value)
        trans.bad_comment= bad_list[i]
        trans.save()
    messages.success(request, 'Success')
    return redirect('/coin/overlord_view')

# def accept_coin(request):
#     id_list = request.POST.getlist('id')
#     accept_list = request.POST.getlist('need_to_accept')
#     badge = request.POST.get('badge_id')
#     for i, value in enumerate(id_list):
#         trans = transaction.objects.get(id=value)
#         give1 = trans.gave
#         agent = employee_id.objects.get(badgeid=trans.recipient)
#         from_agent = employee_id.objects.get(badgeid=trans.benefactor)
#         if int(accept_list[i]):
#             trans.need_to_accept = 1
#             agent.to_accept -= give1
#         else:
#             trans.need_to_accept = 0
#             from_agent.give += give1
#             agent.to_accept -= give1
#             trans.rejected = 1
#         agent.save()
#         from_agent.save()
#         trans.save()
#     return redirect('/coin_sharing/agent')