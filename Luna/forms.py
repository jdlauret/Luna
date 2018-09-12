from django import forms
from django.utils.safestring import mark_safe
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


class SoftSavingsForm(forms.Form):
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

class RTSForm(forms.Form):
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)

<<<<<<< dev_branch
=======
class CSForm(forms.Form):
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)
>>>>>>> Update 2

class FullBenefitForm(forms.Form):
    month = previous_month_end().replace(
        month=previous_month_end().month % 12 + 1,
        day=1,
        year=previous_month_end().year - 1
    )
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)
    twelve_months_consumption = forms.FloatField(
        required=True
    )
    eleven_months_consumption = forms.FloatField(
        required=True
    )
    ten_months_consumption = forms.FloatField(
        required=True
    )
    nine_months_consumption = forms.FloatField(
        required=True
    )
    eight_months_consumption = forms.FloatField(
        required=True
    )
    seven_months_consumption = forms.FloatField(
        required=True
    )
    six_months_consumption = forms.FloatField(
        required=True
    )
    five_months_consumption = forms.FloatField(
        required=True
    )
    four_months_consumption = forms.FloatField(
        required=True
    )
    three_months_consumption = forms.FloatField(
        required=True
    )
    two_months_consumption = forms.FloatField(
        required=True
    )
    one_months_consumption = forms.FloatField(
        required=True
    )
    twelve_months_backfeed = forms.FloatField(
        required=True
    )
    eleven_months_backfeed = forms.FloatField(
        required=True
    )
    ten_months_backfeed = forms.FloatField(
        required=True
    )
    nine_months_backfeed = forms.FloatField(
        required=True
    )
    eight_months_backfeed = forms.FloatField(
        required=True
    )
    seven_months_backfeed = forms.FloatField(
        required=True
    )
    six_months_backfeed = forms.FloatField(
        required=True
    )
    five_months_backfeed = forms.FloatField(
        required=True
    )
    four_months_backfeed = forms.FloatField(
        required=True
    )
    three_months_backfeed = forms.FloatField(
        required=True
    )
    two_months_backfeed = forms.FloatField(
        required=True
    )
    one_months_backfeed = forms.FloatField(
        required=True
    )
    twelve_months_utility_bill = forms.FloatField(
        required=True
    )
    eleven_months_utility_bill = forms.FloatField(
        required=True
    )
    ten_months_utility_bill = forms.FloatField(
        required=True
    )
    nine_months_utility_bill = forms.FloatField(
        required=True
    )
    eight_months_utility_bill = forms.FloatField(
        required=True
    )
    seven_months_utility_bill = forms.FloatField(
        required=True
    )
    six_months_utility_bill = forms.FloatField(
        required=True
    )
    five_months_utility_bill = forms.FloatField(
        required=True
    )
    four_months_utility_bill = forms.FloatField(
        required=True
    )
    three_months_utility_bill = forms.FloatField(
        required=True
    )
    two_months_utility_bill = forms.FloatField(
        required=True
    )
    one_months_utility_bill = forms.FloatField(
        required=True
    )

    labels = {
        'twelve': month.strftime('%b %Y'),
        'eleven': (month + relativedelta(months=1)).strftime('%b %Y'),
        'ten': (month + relativedelta(months=2)).strftime('%b %Y'),
        'nine': (month + relativedelta(months=3)).strftime('%b %Y'),
        'eight': (month + relativedelta(months=4)).strftime('%b %Y'),
        'seven': (month + relativedelta(months=5)).strftime('%b %Y'),
        'six': (month + relativedelta(months=6)).strftime('%b %Y'),
        'five': (month + relativedelta(months=7)).strftime('%b %Y'),
        'four': (month + relativedelta(months=8)).strftime('%b %Y'),
        'three': (month + relativedelta(months=9)).strftime('%b %Y'),
        'two': (month + relativedelta(months=10)).strftime('%b %Y'),
        'one': (month + relativedelta(months=11)).strftime('%b %Y')
    }

    # def grid_fields(self):
    #     pass
    #
    # grid = [
    #     [
    #         month.strftime('%b %Y'),
    #         # twelve_months_consumption,
    #         forms.FloatField(
    #             required=True
    #         ),
    #         twelve_months_backfeed,
    #         twelve_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=1)).strftime('%b %Y'),
    #         eleven_months_consumption,
    #         eleven_months_backfeed,
    #         eleven_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=2)).strftime('%b %Y'),
    #         ten_months_consumption,
    #         ten_months_backfeed,
    #         ten_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=3)).strftime('%b %Y'),
    #         nine_months_consumption,
    #         nine_months_backfeed,
    #         nine_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=4)).strftime('%b %Y'),
    #         eight_months_consumption,
    #         eight_months_backfeed,
    #         eight_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=5)).strftime('%b %Y'),
    #         seven_months_consumption,
    #         seven_months_backfeed,
    #         seven_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=6)).strftime('%b %Y'),
    #         six_months_consumption,
    #         six_months_backfeed,
    #         six_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=7)).strftime('%b %Y'),
    #         five_months_consumption,
    #         five_months_backfeed,
    #         five_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=8)).strftime('%b %Y'),
    #         four_months_consumption,
    #         four_months_backfeed,
    #         four_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=9)).strftime('%b %Y'),
    #         three_months_consumption,
    #         three_months_backfeed,
    #         three_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=10)).strftime('%b %Y'),
    #         two_months_consumption,
    #         two_months_backfeed,
    #         two_months_utility_bill
    #     ],
    #     [
    #         (month + relativedelta(months=11)).strftime('%b %Y'),
    #         one_months_consumption,
    #         one_months_backfeed,
    #         one_months_utility_bill
    #     ]
    # ]


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
