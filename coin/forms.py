from django import forms
from coin.models import employee_id, transaction
from .utilities.user_list import user_list


class statusForm(forms.ModelForm):
    class Meta:
        model = employee_id
        fields = ['name', 'badgeid', 'allotment', 'to_accept', 'edited', ]


class transForm(forms.ModelForm):

    class Meta:
        model = transaction
        fields = ['recipient', 'award', 'note', 'anonymous', ]
        to_id=(
            user_list()
        )
