from django.shortcuts import render

# Create your views here.
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.models import Permission, User, Group
from django.template.context_processors import csrf
from django.template import loader, Context, Template, Library, RequestContext
from django.views.generic import View
from xhtml2pdf import pisa

from .models import CareerPath, AutomatorTask
from .templates.template_updates import JsonHandler
from .forms import SystemPerformanceForm
from .utilities.system_performance_calc import system_performance
from .utilities.page_notes import *

register = Library()


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


def automation_access(user):
    return user.groups.filter(name='Automation Access').exists()


def index(request):
    template = loader.get_template('Luna/index.html')
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
        return HttpResponse(template.render(context))

    else:
        return HttpResponse('/Luna')


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
            template = loader.get_template('Luna/system_performance_calc.html')
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return HttpResponse(template.render(context))
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
                return render(request, 'Luna/system_performance_pdf.html', context=context)
        else:
            form = SystemPerformanceForm()
            template = loader.get_template('Luna/system_performance_pdf.html')
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/Luna')


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@user_passes_test(automation_access)
def automation_page(request):
    return HttpResponse('Woot')