from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class SystemPerformanceForm(forms.Form):
    service_number = forms.CharField(label='Service Number:', max_length=20, required=True)
    start_date = forms.DateField(label='Start Date:',
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'type': 'date'
                                 }))
    end_date = forms.DateField(label='End Date:',
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'type': 'date'
                               }))
