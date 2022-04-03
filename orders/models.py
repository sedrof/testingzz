from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils.functional import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver
from sellers.models import Users



class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    card_first_chars = models.CharField(max_length=50, null=True, blank=True)
    card_id = models.CharField(max_length=50, null=True, blank=True)
    card_type = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    price = models.PositiveSmallIntegerField( null=True, blank=True)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='orders', blank=True)
    sold = models.BooleanField(default=False)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return str(self.owner) + ": " + str(self.price)


class Credit(models.Model):
    credit = models.PositiveSmallIntegerField( null=True, blank=True, validators=[MaxValueValidator(20000)],default=0)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='credits', blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.owner.username) + ": " + str(self.credit)
    class Meta:
        db_table = 'credit'

@receiver(post_save, sender=Users)
def create_credit (sender, instance, created, **kwargs):
    if created:
        Credit.objects.create(owner=instance)