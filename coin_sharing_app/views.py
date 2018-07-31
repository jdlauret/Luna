from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from .models import *
from Luna.models import DataWarehouse
from coin_sharing_app.utilities import find_badge_id

def email_check(user):
    return user.email.endswith('@vivintsolar.com')

@login_required
@user_passes_test(email_check)
def index(request):
    # TODO SHOWS THE AGENT WHO EVERYONE SHARED WITH
    # TODO ALLOWS THE AGENT TO SEE THEIR BALANCE IN SHARING AND TOTAL
    email = request.user.email
    badge_id = find_badge_id(email)
    context = {
        'status_coin': transaction_coin.objects.all
    }
    return render(request, 'global.html', context)

@login_required
@user_passes_test(email_check)
def agent(request):
    # TODO NEEDS TO SHOW THE AGENT WHO THEY SHARED WITH, HOW MUCH AND THE DATE AND REASON
    # TODO ALLOW AGENT TO REDEEM CODE. VERFIES THE REDEMPTION CODE TO STATUS_COIN TABLE
    # TODO SHOWS THE BALANCE THEY HAVE LEFT TO SHARE AND THE TOTAL BALANCE ON THEIR ACCOUNT
    # TODO NEED TO FILTER OUT THE RESULTS TO ONLY JUST THE USER SIGNED IN
    email = request.user.email
    badge_id = find_badge_id(email)
    context = {
        'status_coin': status_coin.objects.all
    }
    return render(request, 'agent_view.html', context)

@login_required
@user_passes_test(email_check)
def transaction(request):
    redemption_code = coinManager.random_string_generator()
    email = request.user.email
    badge_id = find_badge_id(email)
    context = {
        'badge_id': badge_id,
        'user_list': user_list(),
        'redemption_code': redemption_code
    }
    print(request.POST)
    return render(request, 'transaction_window.html', context)


def submit_transaction(request):
    # TODO POST DATA NEEDS TO BE ENTERED INTO DB
    # result = transaction_coin.objects.validate_field(request.POST)
    # print (result)
    # try:
    #     len(result) == 0
    # except:
    #     raise Exception('Fields cannot be blank')
    #     return redirect('/transaction')
    return redirect('/coin_sharing/agent')
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         form = transaction_coin(request.POST)
    #         coin_transaction_id = transaction_coin.objects.create_id(request.POST)
    #  return redirect('/coin_sharing/agent')
