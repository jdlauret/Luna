from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django import forms
from django.utils import timezone
from .models import status, transaction
from .utilities.user_list import user_list
from .utilities.coin_sharing_info import coin_sharing
from Luna.models import DataWarehouse
from coin_sharing_app.utilities import find_badge_id
from coin_sharing_app.forms import statusForm, transForm


def email_check(user):
    return user.email.endswith('@vivintsolar.com')

# TODO NEED TO CREATE AN OVERLORD PAGE
@login_required
@user_passes_test(email_check)
def overlord_view(request):
    context = {
        'transaction': transaction.objects.all,
        'status': status.objects.all,
    }
    return render(request, 'overlord_view.html', context)


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        badge_id = find_badge_id(email)
        agent = status.objects.get(badgeid=badge_id)
        context = {
            'transaction': transaction.objects.all,
            'coin': agent.give,
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
        agent = status.objects.get(badgeid=badge_id)
        context = {
            'alltransaction': transaction.objects.filter(from_id=badge_id).filter(to_id=badge_id),
            'senttransaction': transaction.objects.filter(to_id=badge_id),
            'fromtransaction': transaction.objects.filter(from_id=badge_id),
            'to_accept': transaction.objects.filter(to_id=badge_id).filter(accept=False),
            'status': status.objects.all,
            'coin': agent.give,
        }
        return render(request, 'agent_view.html', context)
    else:
        return HttpResponseRedirect('/Luna')

#TODO NEED TO WORK ON USING MODEL FORMS IN TRANSACTION
@login_required
@user_passes_test(email_check)
def transactions(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = transForm(request.POST)
            if form.is_valid():
                email = request.user.email
                badge_id = find_badge_id(email)
                agent = status.objects.get(badgeid=badge_id)
                context = {
                    'badge_id': badge_id,
                    'user_list': user_list(),
                    'coin': agent.give,
                }

                model_instance = form.save(commit=False)
                model_instance = timestamp = timezone.now()
                model_instance.save()
                return render(request, 'transaction_window.html', context)
        else:
            form = transForm()
        return render(request, "/coin_sharing/transaction", {'form':form})
    else:
        return HttpResponseRedirect('/Luna')


def submit_transaction(request):
    # todo create transaction form
    result = transaction.objects.validate_transaction(request.POST)

    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/coin_sharing/transaction')
    messages.success(request, 'Successfully Submitted Transaction')
    return redirect('/coin_sharing/agent')
