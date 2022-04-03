
from django import forms
from django.contrib.auth.models import User

from .models import Payout



class PayoutCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].required = True
        self.fields['btc_address'].required = True
        self.fields['amount_to_pay'].required = True

    class Meta:
        model = Payout
        fields = ('payment_method', 'amount_to_pay', 'btc_address', 'actual_amount')

