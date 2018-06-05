# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.template import loader, Library, RequestContext

from .models import CareerPath
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

                response = render_to_response('Luna/system_performance_calc.html',
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
        return HttpResponseRedirect('/Luna')


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
        if request.method == 'POST':
            automation_form = AutomatorForm(request.POST)
            data_source_type = automation_form.cleaned_data['data_source_type']
            data_source_location = automation_form.cleaned_data['data_source_location']
            data_source_id = automation_form.cleaned_data['data_source_id']
            data_format_type = automation_form.cleaned_data['data_format_type']
            context = {
                'user': request.user,
                'start_form': automation_form,
                'start_form_completed': True,
                'google_sheet_form': GoogleSheetsFormat(request.POST),
                'csv_form': CsvForm(request.POST),
                'excel_form': ExcelForm(request.POST),
            }
            render_to_response('Luna/system_performance_pdf.html',
                               context,
                               RequestContext(request))
        else:
            context = {
                'user': request.user,
                'start_form': AutomatorForm(),
                'google_sheet_form': GoogleSheetsFormat(),
                'csv_form': CsvForm(),
                'excel_form': ExcelForm(),
            }
            return render(request, 'Luna/automation.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(automation_access)
def create_new_task(request):
    context = {'user': request.user}
    return render(request, 'Luna/automation_create_new_task.html', context)