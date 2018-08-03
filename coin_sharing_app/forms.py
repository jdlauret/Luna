from django.db import models
from django.forms import ModelForm
from coin_sharing_app.models import status, transaction


class statusForm(ModelForm):
    class Meta:
        model = status
        fields = ['name', 'badgeid', 'give', 'to_accept', 'edited']


class transForm(ModelForm):

    class Meta:
        model = transaction
        fields = ['to_id', 'gave', 'created_at', 'note', 'anonymous',]
