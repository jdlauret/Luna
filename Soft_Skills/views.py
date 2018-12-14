from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Soft_Skills.utilities.supervisor_list import supervisor_list
from .models import Employee_List


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            super_list = request.POST.getlist('super_badge')
            super_list = list(map(int, super_list))
            print(request.POST)
            context = {
                'supervisor_list' : supervisor_list(),
                'super_badge' : super_list,
                'employee_list' : Employee_List.objects.all().filter(supervisor_badge__in=super_list, terminated=False),
            }
            return render(request, 'soft_skills.html', context)
        else:
            context = {
                'supervisor_list' : supervisor_list(),
            }
            return render(request, 'soft_skills.html', context)
    else:
        return HttpResponseRedirect('/Luna')