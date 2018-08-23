from django.forms import ModelForm
from django import forms

from coin.models import employee_id, transaction
from .utilities.user_list import user_list

class transactionForm(ModelForm):
    class Meta:
        ANONYMOUS_CHOICES = (
            (0, 'No'),
            (1, 'Yes'),
        )
        model = transaction
        fields = [ 'anonymous']
        widgets = {
            'anonymous': forms.Select(choices=ANONYMOUS_CHOICES)
        }