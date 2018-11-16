from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from Soft_Skills.utilities.employee_list import employee_list
from .models import Career_Path, Employee_List, Agent_Skills


def index(request):
    context = {
        'supervisor_list' : Employee_List.objects.filter(terminated=False),

    }
    return render(request, 'soft_skills.html', context)

