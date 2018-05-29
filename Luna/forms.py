from django import forms
from datetime import date
from dateutil.relativedelta import relativedelta


class DateInput(forms.DateInput):
    input_type = 'date'


def previous_month():
    today = date.today()
    return date(today.year, today.month, 1) - relativedelta(days=1)


class SystemPerformanceForm(forms.Form):
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)
    start_date = forms.DateField(label='Start Date:',
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'type': 'date'
                                 }))
    end_date = forms.DateField(label='End Date:',
                               initial=previous_month(),
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'type': 'date'
                               }))
