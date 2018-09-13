from django import forms
from coin.models import employee_id, transaction

class transactionForm(forms.ModelForm):
    recipient = forms.IntegerField(label='Recipient')
    award = forms.IntegerField(label='Award')
    note = forms.TextInput(label='Note')

    class Meta:
        model = transaction
        fields = ['recipient', 'award', 'note']