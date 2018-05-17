from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Permission, User
from django.template import loader, Context, Template, Library
from .models import CareerPath, AutomatorTask
from django.db.models import Max
from collections import OrderedDict

register = Library()


def index(request):
    template = loader.get_template('Luna/index.html')
    context = {'user': request.user}
    return HttpResponse(template.render(context))


def career_path(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/career_path.html')
        context = {
            'user': request.user,
            'career_path_data': build_career_path(),
            'job_description': CareerPath.objects.all()
        }
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('/Luna')


def system_performance_calculator(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/system_performance_calc.html')
        context = {'user': request.user}
        return HttpResponse(template.render(context={'user': request.user}))
    else:
        return HttpResponseRedirect('/Luna')


def build_career_path():
    departments = [x['department'] for x in CareerPath.objects.order_by().values('department').distinct()]

    new_dict = {}
    most_rows = int(CareerPath.objects.all().aggregate(Max('tier_level'))['tier_level__max'])
    most_cols = int(str(CareerPath.objects.all().aggregate(Max('tier_level'))['tier_level__max'])
                    .split('.')[1]) + 1
    for department in departments:
        department_key = department.replace('_', ' ').title()
        positions = CareerPath.objects.filter(department=department).order_by('tier_level').values()
        functions = list(set([x['function'] for x in positions]))
        max_tier = int(max(x['tier_level'] for x in positions))
        if max_tier > most_rows:
            most_rows = max_tier
        new_dict[department_key] = {}

        for i, function in enumerate(functions):
            function_key = function.replace('_', ' ').title()
            new_dict[department_key][function_key] = {}

            for i in range(most_rows):
                if i == 0:
                    new_dict[department_key][function_key][i + 1] = [{'position': function_key}]
                else:
                    new_dict[department_key][function_key][i + 1] = [{'position': ''}]

        for position in positions:
            column = str(position['tier_level']).split('.')[0]
            row = str(position['tier_level']).split('.')[1]
            function_key = position['function'].replace('_', ' ').title()

            if len(new_dict[department_key][function_key][int(row)]) < int(column):
                for i in range(int(column) - 1):
                    new_dict[department_key][function_key][int(row)].append({'position': ''})
            position_data = {
                'position': position['position'].replace('_', ' ').title(),
                'id': position['id'],
                'position_data': position
            }
            new_dict[department_key][function_key][int(row)].append(position_data)

    for department, value in new_dict.items():
        for function, value2 in value.items():
            for row_num, value3 in value2.items():
                for i in range(most_cols):
                    if len(value3) < most_cols:
                        value3.append({'position': ''})

    rts_key_order = ['Inbound', 'Auxiliary', 'Super Agent', 'Service']
    customer_solutions_order = ['Specialist 1', 'Super Agent']
    relations_order = ['Inbound Outbound', 'Email Admin', 'Documents']
    new_dict['Real Time Scheduling'] = OrderedDict(sorted(new_dict['Real Time Scheduling'].items(),
                                                          key=lambda j: rts_key_order.index(j[0])))
    new_dict['Customer Solutions'] = OrderedDict(sorted(new_dict['Customer Solutions'].items(),
                                                        key=lambda j: customer_solutions_order.index(j[0])))
    new_dict['Relations'] = OrderedDict(sorted(new_dict['Relations'].items(),
                                               key=lambda j: relations_order.index(j[0])))

    return new_dict
