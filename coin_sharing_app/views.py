from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.template import loader, Library, RequestContext

from .utilities.coin_sharing_info import *
from coin_sharing_app.utilities.user_list import *
from .models import *
from Luna.models import DataWarehouse
import datetime

def email_check(user):

    return user.email.endswith('@vivintsolar.com')

@login_required
@user_passes_test(email_check)
def index(request):
    context={
        'coin_status': coin_status.objects.all,
        # 'coin_transaction': coin_transaction.objects.all
    }
    x = datetime.datetime.now()
    print(x)
    return render(request, 'global.html', context)

def agent(request):
    context={
        # 'coin_status': coin_status.objects.all,
        'coin_transaction': coin_transaction.objects.all
    }
    return render (request, 'agent_view.html', context)

def transaction(request):
    redemption_code = coinManager.random_string_generator()
    context = {
        'user_list': user_list(),
        'redemption_code': redemption_code,
    }
    return render ( request, 'transaction_window.html', context)

def submit_transaction(request):
    coin_transaction_id = coin_transaction.objects.create_id(request.POST)
    return redirect('agent_view')