from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import employee_id, transaction
from .utilities.user_list import user_list
from .utilities.agent_name import agent_name
from coin.utilities import find_badge_id


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge_id = find_badge_id(email)
        agent = employee_id.objects.get(badgeid=badge_id)
        context = {
            'transaction': reversed(transaction.objects.all().order_by('created_at')[:50]),
            'coin': agent.allotment,
            # 'agent_name': agent_name(transaction.objects.get(benefactor=agent))
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
        context = {
            'alltransaction': reversed(transaction.objects.all().order_by('created_at')[:50]), #View All
            'senttransaction': reversed(transaction.objects.filter(recipient=badge_id).order_by('created_at')[:50]), #View Sent
            'fromtransaction': reversed(
                transaction.objects.filter(benefactor=badge_id).order_by('created_at')[:50]), #View received
            # 'need_to_accept': reversed(
            #     transaction.objects.filter(recipient=badge_id).filter(need_to_accept=0).filter(rejected=0).order_by(
            #         'created_at')[:50]), #View Accepted Coins
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
    # todo badge_id needs to link to employee_id model
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
        return redirect('/coin_sharing/transaction')
    messages.success(request, 'Success')
    return redirect('/coin_sharing/transaction')


# TODO NEED TO CREATE AN OVERLORD PAGE
@login_required
@user_passes_test(email_check)
def overlord_view(request):
    context = {
        'transaction': transaction.objects.all,
        'employee_id': employee_id.objects.all,
    }
    return render(request, 'overlord_view.html', context)

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