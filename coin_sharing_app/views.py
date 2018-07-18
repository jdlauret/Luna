from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.template import loader, Library, RequestContext

from .utilities.coin_sharing_info import *
from .utilities.user_list import *
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
        'badge_id': user_list(),
        'full_name':user_list()
    }

    return render ( request, 'transaction_window.html', context)

