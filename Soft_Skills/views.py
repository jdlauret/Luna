from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from Soft_Skills.utilities.employee_list import employee_list
from Soft_Skills.utilities.supervisor_list import supervisor_list
from .models import Career_Path, Employee_List, Agent_Skills


def index(request):
    context = {
        'supervisor_list' : supervisor_list(),
    }
    list = Employee_List.objects.filter(terminated=False).distinct('supervisor_badge')
    print(list, type(list))
    return render(request, 'soft_skills.html', context)

