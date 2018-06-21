# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response, HttpResponse, get_object_or_404, redirect
from django.template import loader, Library, RequestContext
from django.core import serializers

from Luna.utilities.template_updates import JsonHandler
from .forms import *
from .utilities.system_performance_calc import system_performance
from .utilities.page_notes import *

register = Library()


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


def automation_access(user):
    return user.groups.filter(name='Automation Access').exists()


def index(request):
    context = {'user': request.user}
    return render(request, 'Luna/index.html', context)


@login_required
@user_passes_test(email_check)
def career_path(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/career_path.html')

        context = {
            'user': request.user,
            'career_path_data': JsonHandler().get_json('career_path.json'),
            'job_description': CareerPath.objects.all()

        }
        return render(request, 'Luna/career_path.html', context=context)

    else:
        return render(request, 'Luna/index.html')


@login_required
@user_passes_test(email_check)
def system_performance_calculator(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SystemPerformanceForm(request.POST)
            if form.is_valid():
                service_number = form.cleaned_data['service_number']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                # TODO pass parameters to Mack's function
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': True,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                try:
                    results = system_performance(service_number, start_date, end_date)
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render(request, 'Luna/system_performance_calc.html', context=context)
                return response
            else:
                form = SystemPerformanceForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/system_performance_calc.html', context=context)
        else:
            form = SystemPerformanceForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/system_performance_calc.html', context)
    else:
        return HttpResponseRedirect('/')


@login_required
@user_passes_test(email_check)
def performance_calculator_print(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SystemPerformanceForm(request.POST)
            if form.is_valid():
                service_number = form.cleaned_data['service_number']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                # TODO pass parameters to Mack's function
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': True,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                try:
                    results = system_performance(service_number, start_date, end_date)
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render_to_response('Luna/system_performance_pdf.html',
                                              context,
                                              RequestContext(request))
                return response
            else:
                form = SystemPerformanceForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/system_performance_pdf.html', context)
        else:
            form = SystemPerformanceForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/system_performance_pdf.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(automation_access)
def automation_page(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user
        }
        return render(request, 'Luna/automation.html', context)
    else:
        return HttpResponseRedirect('/')


@login_required
@user_passes_test(automation_access)
def create_new_task(request):
    if request.user.is_authenticated:
        context = {'user': request.user}
        if request.method == 'POST':
            form = AutomatorForm(request.POST)
            context['form'] = form
            if form.is_valid():
                return render(request, 'Luna/automation_view_existing_tasks.html', context)
            else:
                return render(request, 'Luna/automation_create_new_task.html', context)
        else:
            context['form'] = AutomatorForm()
            return render(request, 'Luna/automation_create_new_task.html', context)
    else:
        return HttpResponseRedirect('/')


@login_required
@user_passes_test(email_check)
def vcaas_data_set(request):
    model_data = create_table_from_model(VcaasLogin)
    context = {
        'form': VcaasForm(),
        'model_data': model_data,
        'update_model': ''
    }
    return render(request, 'Luna/vcaas_data.html', context)


def vcaas_update(request, id=None):
    if request.user.is_authenticated:
        print('authenticated')
        if request.POST == 'POST':
            model_data = create_table_from_model(VcaasLogin)
            form = VcaasForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/wfm/vcaas')
            else:
                model_data = create_table_from_model(VcaasLogin)
                context = {
                    'form': form,
                    'model': model_data,
                    'update_model': '',
                }
                update_object = context['model'][id]
                context['update_model'] = update_object
                return render(request, 'Luna/vcaas_update_form.html', context)
        else:
            print('else')
            print(id)
            if id is None:
                form = VcaasForm()
                context = {'form': form}
                return render(request, 'Luna/vcaas_update_form.html', context)
            else:
                try:
                    id = int(id)
                    id_is_number = True
                except ValueError:
                    id_is_number = False

                if id_is_number:
                    form = VcaasForm(request.POST)
                    model_data = create_table_from_model(VcaasLogin)
                    context = {
                        'form': form,
                        'model': model_data,
                        'update_model': '',
                    }
                    update_object = context['model'][id]
                    context['update_model'] = update_object
                    return render(request, 'Luna/vcaas_update_form.html', context)
                else:
                    form = VcaasForm(request.POST, id=id)
                    context = {'form': form}
                    return render(request, 'Luna/vcaas_update_form.html', context)


def wfm(request):
    context = {'user': request.user}
    return render(request, 'Luna/workforce_tools.html', context)


def create_table_from_model(model):
    model_fields = [x.name for x in model._meta.get_fields()]
    model_header = [x.replace('_', ' ').title() for x in model_fields]
    model_list = []

    for item in model.objects.all():
        new_row = []
        for field in model_fields:
            new_row.append(item.__dict__[field])
        model_list.append(new_row)

    data = {
        'fields': model_fields,
        'header': model_header,
        'table': model_list
    }

    return data


