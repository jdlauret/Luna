# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.template import loader, Library, RequestContext
from django.contrib.auth.models import Group

from .models import CareerPath
from Luna.utilities.template_updates import JsonHandler
from .forms import *
from .utilities.soft_savings_analysis import soft_savings_analysis
from .utilities.full_benefit_analysis import full_benefit_analysis
from .utilities.system_performance_calc import system_performance
from .utilities.page_notes import *
from .utilities.RTS_notes_wizard import notes_wizard

register = Library()


def email_check(user):
    return user.email.endswith('@vivintsolar.com')


def automation_access(user):
    return user.groups.filter(name='Automation Access').exists()

def overlord_access(user):
    return user.groups.filter(name='Coin_Overlord').exists()

def index(request):
    context = {
        # 'user': request.user
    }
    return render(request, 'Luna/index.html', context)


@login_required
@user_passes_test(email_check)
def career_path(request):
    if request.user.is_authenticated:

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
                    results = system_performance(str(service_number), str(start_date), str(end_date))
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
                    results = system_performance(str(service_number), str(start_date), str(end_date))
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


@login_required
@user_passes_test(email_check)
def full_benefit_calculator(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = FullBenefitForm(request.POST)
            if form.is_valid():
                service_number = form.cleaned_data['service_number']
                consumption = [
                    abs(form.cleaned_data['twelve_months_consumption']),
                    abs(form.cleaned_data['eleven_months_consumption']),
                    abs(form.cleaned_data['ten_months_consumption']),
                    abs(form.cleaned_data['nine_months_consumption']),
                    abs(form.cleaned_data['eight_months_consumption']),
                    abs(form.cleaned_data['seven_months_consumption']),
                    abs(form.cleaned_data['six_months_consumption']),
                    abs(form.cleaned_data['five_months_consumption']),
                    abs(form.cleaned_data['four_months_consumption']),
                    abs(form.cleaned_data['three_months_consumption']),
                    abs(form.cleaned_data['two_months_consumption']),
                    abs(form.cleaned_data['one_months_consumption'])
                ]
                backfeed = [
                    abs(form.cleaned_data['twelve_months_backfeed']),
                    abs(form.cleaned_data['eleven_months_backfeed']),
                    abs(form.cleaned_data['ten_months_backfeed']),
                    abs(form.cleaned_data['nine_months_backfeed']),
                    abs(form.cleaned_data['eight_months_backfeed']),
                    abs(form.cleaned_data['seven_months_backfeed']),
                    abs(form.cleaned_data['six_months_backfeed']),
                    abs(form.cleaned_data['five_months_backfeed']),
                    abs(form.cleaned_data['four_months_backfeed']),
                    abs(form.cleaned_data['three_months_backfeed']),
                    abs(form.cleaned_data['two_months_backfeed']),
                    abs(form.cleaned_data['one_months_backfeed'])
                ]
                utility_bill = [
                    form.cleaned_data['twelve_months_utility_bill'],
                    form.cleaned_data['eleven_months_utility_bill'],
                    form.cleaned_data['ten_months_utility_bill'],
                    form.cleaned_data['nine_months_utility_bill'],
                    form.cleaned_data['eight_months_utility_bill'],
                    form.cleaned_data['seven_months_utility_bill'],
                    form.cleaned_data['six_months_utility_bill'],
                    form.cleaned_data['five_months_utility_bill'],
                    form.cleaned_data['four_months_utility_bill'],
                    form.cleaned_data['three_months_utility_bill'],
                    form.cleaned_data['two_months_utility_bill'],
                    form.cleaned_data['one_months_utility_bill']
                ]
                # TODO pass parameters to Mack's function
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': True,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                try:
                    results = full_benefit_analysis(service_number, consumption, backfeed, utility_bill)
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render(request, 'Luna/full_benefit_analysis.html', context=context)

                return response
            else:
                form = FullBenefitForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/full_benefit_analysis.html', context=context)
        else:
            form = FullBenefitForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/full_benefit_analysis.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def full_benefit_print(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = FullBenefitForm(request.POST)
            if form.is_valid():
                service_number = form.cleaned_data['service_number']
                consumption = [
                    form.cleaned_data['twelve_months_consumption'],
                    form.cleaned_data['eleven_months_consumption'],
                    form.cleaned_data['ten_months_consumption'],
                    form.cleaned_data['nine_months_consumption'],
                    form.cleaned_data['eight_months_consumption'],
                    form.cleaned_data['seven_months_consumption'],
                    form.cleaned_data['six_months_consumption'],
                    form.cleaned_data['five_months_consumption'],
                    form.cleaned_data['four_months_consumption'],
                    form.cleaned_data['three_months_consumption'],
                    form.cleaned_data['two_months_consumption'],
                    form.cleaned_data['one_months_consumption']
                ]
                backfeed = [
                    form.cleaned_data['twelve_months_backfeed'],
                    form.cleaned_data['eleven_months_backfeed'],
                    form.cleaned_data['ten_months_backfeed'],
                    form.cleaned_data['nine_months_backfeed'],
                    form.cleaned_data['eight_months_backfeed'],
                    form.cleaned_data['seven_months_backfeed'],
                    form.cleaned_data['six_months_backfeed'],
                    form.cleaned_data['five_months_backfeed'],
                    form.cleaned_data['four_months_backfeed'],
                    form.cleaned_data['three_months_backfeed'],
                    form.cleaned_data['two_months_backfeed'],
                    form.cleaned_data['one_months_backfeed']
                ]
                utility_bill = [
                    form.cleaned_data['twelve_months_utility_bill'],
                    form.cleaned_data['eleven_months_utility_bill'],
                    form.cleaned_data['ten_months_utility_bill'],
                    form.cleaned_data['nine_months_utility_bill'],
                    form.cleaned_data['eight_months_utility_bill'],
                    form.cleaned_data['seven_months_utility_bill'],
                    form.cleaned_data['six_months_utility_bill'],
                    form.cleaned_data['five_months_utility_bill'],
                    form.cleaned_data['four_months_utility_bill'],
                    form.cleaned_data['three_months_utility_bill'],
                    form.cleaned_data['two_months_utility_bill'],
                    form.cleaned_data['one_months_utility_bill']
                ]
                # TODO pass parameters to Mack's function
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': True,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                try:
                    results = full_benefit_analysis(service_number, consumption, backfeed, utility_bill)
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render_to_response('Luna/full_benefit_analysis_pdf.html',
                                              context,
                                              RequestContext(request))
                return response
            else:
                form = FullBenefitForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/full_benefit_analysis_pdf.html', context)
        else:
            form = FullBenefitForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/full_benefit_analysis_pdf.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def soft_savings_calculator(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SoftSavingsForm(request.POST)
            if form.is_valid():
                print('form is valid')
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
                    results = soft_savings_analysis(str(service_number), str(start_date), str(end_date))
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render(request, 'Luna/soft_savings_analysis.html', context=context)

                return response
            else:
                form = SoftSavingsForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/soft_savings_analysis.html', context=context)
        else:
            form = SystemPerformanceForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/soft_savings_analysis.html', context)
    else:
        return HttpResponseRedirect('/Luna')


@login_required
@user_passes_test(email_check)
def soft_savings_print(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SoftSavingsForm(request.POST)
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
                    results = soft_savings_analysis(str(service_number), str(start_date), str(end_date))
                    context['form_response'] = results
                except Exception as e:
                    context['form_response_complete'] = False

                response = render_to_response('Luna/soft_savings_analysis_pdf.html',
                                              context,
                                              RequestContext(request))
                return response
            else:
                form = SoftSavingsForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                    'legal_footer': print_page_legal_footer,
                }
                return render(request, 'Luna/soft_savings_analysis_pdf.html', context)
        else:
            form = SoftSavingsForm()
            context = {
                'user': request.user,
                'form': form,
                'form_response_complete': False,
                'form_response': {},
                'legal_footer': print_page_legal_footer,
            }
            return render(request, 'Luna/soft_savings_analysis_pdf.html', context)
    else:
        return HttpResponseRedirect('/Luna')

# Rework this code to fit RTS Wizard notes
@login_required
@user_passes_test(email_check)
def RTS_notes (request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RTSForm(request.POST)
            if form.is_valid():
                service_number = form.cleaned_data['service_number']
                context = {
                    # Form contains Name=Service Number, Value = .... Maxlength=20
                    'form': form,
                    # User contains person who signed into Luna
                    'user': request.user,
                    'form_response_complete': True,
                    # Dictionary from function notes_wizard, plus tsr, num_modules, azimuth, and tilt
                    'form_response': notes_wizard(service_number)
                }
                response = render(request, 'Luna/RTS_notes_wizard.html', context=context)
                return response
            else:
                form = RTSForm()
                context = {
                    'form': form,
                    'user': request.user,
                    'form_response_complete': False,
                    'form_response': {},
                }
                return render(request, 'Luna/RTS_notes_wizard.html', context=context)
        else:
            form = RTSForm()
            context = {
                'form': form,
                'user': request.user,
                'form_response_complete': False,
                'form_response': {},
            }
            return render(request, 'Luna/RTS_notes_wizard.html', context)
    else:
        return HttpResponseRedirect('/Luna')
