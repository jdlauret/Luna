from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
# @user_passes_test(email_check)
def index(request):
	return render(request, 'main.html')