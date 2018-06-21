from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from .models import *
from datetime import date
from dateutil.relativedelta import relativedelta


class DateInput(forms.DateInput):
    input_type = 'date'


def previous_month_end():
    today = date.today()
    return date(today.year, today.month, 1) - relativedelta(days=1)


def previous_month_start():
    pass


class SystemPerformanceForm(forms.Form):
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)
    start_date = forms.DateField(label='Start Date:',
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'type': 'date'
                                 }))
    end_date = forms.DateField(label='End Date:',
                               initial=previous_month_end(),
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'type': 'date',
                                   'width': '100%',
                               }))


class AutomatorForm(ModelForm):
    class Meta:
        model = AutomatorTask
        fields = [
            'task_name',
            'recurrence_type',
            'recurrence_month_days',
            'recurrence_week_days',
            'recurrence_times',
            'recurrence_minutes',
            'recurrence_months',
            'recurrence_weeks',
            'recurrence_start_date',
            'data_source_type',
            'data_source_google_id',
            'data_format_type',
            'data_format_google_id',
            'file_name',
            'dynamic_file_name',
            'spreadsheet_sheet_name',
            'spreadsheet_start_column_number',
            'spreadsheet_start_row_number',
            'spreadsheet_end_column_number',
            'spreadsheet_end_row_number',
            'file_storage_type',
            'file_storage_google_id',
        ]


class VcaasForm(ModelForm):
    class Meta:
        model = VcaasLogin
        fields = [
            'first_name',
            'last_name',
            'badge',
            'incontact_id',
            'email',
            'department',
            'psuedo_number',
            'phone_number',
            'user_id',
            'id',
            'vcaas_password',
            'voice_mail_passcode',
            'extension',
            'voice_mail',
            'dnis_enabled'
        ]