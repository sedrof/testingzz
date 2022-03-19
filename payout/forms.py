
from django import forms
from django.contrib.auth.models import User

from .models import Payout



class PayoutCreateForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = ('payment_method', 'amount_to_pay', 'btc_address', 'actual_amount')

