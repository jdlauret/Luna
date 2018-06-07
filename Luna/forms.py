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


class AutomatorForm(forms.Form):
    DATA_SOURCE_TYPE_CHOICES = (
        ('sql_query', 'SQL Query'),
        ('sql_command', 'SQL Command'),
        ('python_script', 'Python Script')
    )
    DATA_SOURCE_LOCATION_CHOICES = (
        # ('local', 'On your computer'),
        ('google_drive', 'On Google Drive'),
    )
    DATE_FORMAT_TYPE_CHOICES = (
        ('google_sheets', 'Google Sheets'),
        ('excel', 'Excel Workbook'),
        ('csv', 'CSV'),
    )

    DATA_SOURCE_TYPE_HELP = '''SQL Query: A SQL statement to be run with results to be processed\n
    SQL Command: A SQL Statement to be executed in the database with not results to be processed\n
    Python Script: A a python script to be executed'''
    DATA_SOURCE_LOCATION_HELP = """You can choose to upload a file from your computer 
    or select one from Google Drive."""

    data_source_type = forms.ChoiceField(
        label='What type of request is this?: ',
        choices=DATA_SOURCE_TYPE_CHOICES,
        required=True,
        help_text=DATA_SOURCE_TYPE_HELP
    )
    data_source_location = forms.ChoiceField(
        label='Where is the file located?: ',
        choices=DATA_SOURCE_LOCATION_CHOICES,
        help_text=DATA_SOURCE_LOCATION_HELP
    )
    data_source_id = forms.CharField(
        label='Google File ID: '
    )
    data_format_type = forms.ChoiceField(
        label='What format do you want your data in?: ',
        choices=DATE_FORMAT_TYPE_CHOICES,
    )


class GoogleSheetsFormat(forms.Form):
    google_sheet_id = forms.CharField(
        required=True,
        label='Google Sheet ID: '
    )
    sheet_name = forms.CharField(
        required=True,
        label='Sheet Name: '
    )
    starting_column_number = forms.IntegerField(
        required=True
    )
    starting_row_number = forms.IntegerField(
        required=True
    )
    end_column_number = forms.IntegerField()
    end_row_number = forms.IntegerField()


class ExcelForm(forms.Form):
    DYNAMIC_NAME_HELP = """<a href="http://strftime.org/">Click Here</a> for a formatting legend"""

    master_workbook = forms.BooleanField()
    master_workbook_id = forms.CharField(
        label='Existing Master Workbook Google Drive ID: '
    )
    workbook_name = forms.CharField(
        required=True,
        label='Workbook Name: '
    )
    sheet_name = forms.CharField(
        required=True,
        label='Sheet Name: '
    )
    starting_column_number = forms.IntegerField(
        required=True,
        label='Starting Column Number'
    )
    starting_row_number = forms.IntegerField(
        required=True,
        label='Starting Row Number'
    )
    end_column_number = forms.IntegerField(
        label='End Column Number (optional): '
    )
    end_row_number = forms.IntegerField(
        label='End Row Number (optional): '
    )
    dynamic_workbook_name = forms.BooleanField(
        label='Do you want a dynamic name?: '
    )
    dynamic_workbook_name_format = forms.CharField(
        label='Dynamic Name Format',
        help_text=mark_safe(DYNAMIC_NAME_HELP)
    )
    google_drive_folder_id = forms.CharField(
        required=True,
        label='Where in Google Drive do you want the file Stored?: '
    )


class CsvForm(forms.Form):
    DYNAMIC_NAME_HELP = """<a href="http://strftime.org/">Click Here</a> for a formatting legend"""
    csv_name = forms.CharField(
        required=True,
        label='CSV File Name: '
    )
    dynamic_csv_name = forms.BooleanField(
        label='Do you want a dynamic name?: '
    )
    dynamic_csv_name_format = forms.CharField(
        help_text=mark_safe(DYNAMIC_NAME_HELP),
        label='Dynamic Name Format'
    )
    google_drive_folder_id = forms.CharField(
        required=True,
        label='Where in Google Drive do you want the file Stored?: '
    )


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