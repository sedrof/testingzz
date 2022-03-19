from django.db import models

# Create your models here.


class Wallet(models.Model):

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    address = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + ":     " + str(self.address)
