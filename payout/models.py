from django.db import models
from django.utils.functional import cached_property
from sellers.models import *




class Payout(models.Model):
    Amount_Choices = (('Full Amount', 'Full Amount'), ('Specific Amount', 'Specific Amount'),
    )

    Status_Choices = (('Pending', 'Pending'), ('Done', 'Done'),
    )

    Paymnent_Choices = (("BTC", "BTC"),)

    payment_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users,
                              related_name='payout_user',
                              blank=True,
                              null=True,
                              verbose_name='payout_user', on_delete=models.CASCADE)

    btc_address = models.CharField(max_length=150, blank=True, null=True)
    amount_to_pay = models.CharField(max_length=15, choices=Amount_Choices, null=True, blank=True)
    status = models.CharField(max_length=11, choices=Status_Choices, null=True, blank=True, default="Pending")
    payment_method = models.CharField(max_length=10, choices=Paymnent_Choices, null=True, blank=True, default='BTC')
    actual_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


    @cached_property
    def amount_paid(self):
        if self.amount_to_pay == 'Full Amount':
            return str('Full Amount')
        elif self.amount_to_pay == 'Specific Amount':
            return self.actual_amount
        else:
            return None
