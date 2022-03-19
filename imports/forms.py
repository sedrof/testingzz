
import csv
from django import forms


class DataInput(forms.Form):
    file = forms.FileField()
