from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect

from P_Tracker.utilities.find_badge_id import find_badge_id
from P_Tracker.utilities.find_name import find_name

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
		context = {
			'name': name,
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
		context = {
			'name': name,
		}
		return render(request, 'employee.html', context)
	else:
		return HttpResponseRedirect('/Luna')

