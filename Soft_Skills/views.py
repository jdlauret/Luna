import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from Soft_Skills.utilities.employee_list import employee_list
from Soft_Skills.utilities.supervisor_list import supervisor_list
from .models import Career_Path, Employee_List, Agent_Skills


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


@login_required
@user_passes_test(email_check)
def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            super_list = request.POST.getlist('super_badge')
            super_list = list(map(int, super_list))
            context = {
                'supervisor_list' : supervisor_list(),
                'super_badge' : super_list,
                'employee_list' : Employee_List.objects.filter(supervisor_badge__in=super_list, terminated=False),
            }
            return render(request, 'soft_skills.html', context)
        else:
            context = {
                'supervisor_list' : supervisor_list(),
            }
            return render(request, 'soft_skills.html', context)
    else:
        return HttpResponseRedirect('/Luna')

@login_required
@user_passes_test(email_check)
def agent_skills_sheet(request):
    if request.user.is_authenticated:
        print(request.POST)
        selected_employee = int(request.POST['selected_employee'])

        if request.method == 'POST':
            try:
                skill_set = request.POST['select_team']
                customer_relations = Career_Path.objects.filter(team='customer_relations')
                recs_and_rebate = Career_Path.objects.filter(team='RECs_&_rebates')
                central_scheduling = Career_Path.objects.filter(team='central_scheduling')
                customer_solutions = Career_Path.objects.filter(team='customer_solutions')
                customer_service = Career_Path.objects.filter(team='customer_service')
                print('TRY')
                # todo remove print
                if skill_set == 'customer_relations':
                    try:
                        skills_id = request.POST['skills_id']
                    except:
                        context={
                            'skill_set' : skill_set,
                            'selected_employee' : Employee_List.objects.all().get(badge_id=selected_employee),
                            'customer_relations_inbound': customer_relations.filter(sub_team='inbound_outbound').order_by('id'),
                            'customer_relations_rep_1': customer_relations.filter(sub_team='inbound_outbound', tier='rep_1').order_by('id'),
                            'customer_relations_rep_2': customer_relations.filter(sub_team='inbound_outbound', tier='rep_2').order_by('id'),
                            'customer_relations_rep_3': customer_relations.filter(sub_team='inbound_outbound', tier='rep_3').order_by('id'),
                            'customer_relations_specialist_1': customer_relations.filter(sub_team='inbound_outbound', tier='specialist_1').order_by('id'),
                            'customer_relations_specialist_2': customer_relations.filter(sub_team='inbound_outbound', tier='specialist_2').order_by('id'),
                            'customer_relations_specialist_3': customer_relations.filter(sub_team='inbound_outbound', tier='specialist_3').order_by('id'),
                            'customer_relations_team': customer_relations.filter(sub_team='inbound_outbound', tier='team_lead').order_by('id'),
                        }
                        return render(request, 'agent_skill_set.html', context)
                if skill_set == 'RECs_&_rebates':
                    context={
                        'selected_employee' : Employee_List.objects.all().get(badge_id=selected_employee),
                        'recs_and_rebate' : recs_and_rebate,
                    }
                    return render(request, 'agent_skill_set.html', context)
                if skill_set == 'central_scheduling':
                    context={
                        'selected_employee' : Employee_List.objects.all().get(badge_id=selected_employee),
                        'central_scheduling' : central_scheduling,
                    }
                    return render(request, 'agent_skill_set.html', context)
                if skill_set == 'customer_solutions':
                    context={
                        'selected_employee' : Employee_List.objects.all().get(badge_id=selected_employee),
                        'customer_solutions' : customer_solutions,
                    }
                    return render(request, 'agent_skill_set.html', context)
                if skill_set == 'customer_service':
                    context = {
                        'selected_employee': Employee_List.objects.all().get(badge_id=selected_employee),
                        'customer_service': customer_service,
                    }
                    return render(request, 'agent_skill_set.html', context)
                else:
                    return HttpResponseRedirect('/Soft_Skills/')
            except:
                context={
                    'selected_employee' : Employee_List.objects.all().get(badge_id=selected_employee),
                }
                # todo remove print
                print('Except')
                return render(request, 'agent_skill_set.html', context)
        else:
            return HttpResponseRedirect('/Soft_Skills/')
    else:
        return HttpResponseRedirect('/Luna')

# ADDS SOFT SKILL ID TO AGENT SKILLS LIST
def add_soft_skills(request):
    print(request.POST)
    selected_employee = int(request.POST['selected_employee'])
    return redirect('/Soft_Skills/employee', selected_employee=selected_employee)
# todo need to have the user reload the page with new data