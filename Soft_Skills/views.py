from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from Soft_Skills.utilities.employee_list import employee_list


def index(request):
    context = {
        'employee_list' : employee_list(),
    }
    return render(request, 'soft_skills.html', context)

