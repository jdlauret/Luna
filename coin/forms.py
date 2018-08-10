from django import forms
from coin.models import employee_id, transaction

class employeeForm(forms.ModelForm):
    class Meta:
        model = employee_id
        fields = ('name', 'badge_id', 'allotment', 'edited')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = employee_id.objects.name()