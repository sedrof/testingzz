
from django import forms
from .models import *

class BatchEditForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = (
                  'status',)