from django.db import models
from payout.models import Payout
from sellers.models import Users
from django.utils.functional import cached_property


class Country(models.Model):
    code = models.CharField(max_length=6, null=True, blank=True)
    name = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return str(self.code)[0:6] + ": " + str(self.name)

    class Meta(object):
        verbose_name = "Country Codes"
        verbose_name_plural = "Country Codes"
        abstract = False
        db_table = "Country And Codes"


class Batch(models.Model):
    Status_Choices = (
        ("Stop", "Stop"),
        ("Working", "Working"),
    )
    name = models.CharField(max_length=35, null=True, blank=True, unique=True)
    status = models.CharField(
        max_length=11, choices=Status_Choices, null=True, blank=True, default="Working"
    )

    def __str__(self):
        return str(self.name)

    class Meta(object):
        verbose_name = "Batch"
        verbose_name_plural = "Batch"
        abstract = False
        db_table = "Batch"

    # def save(self, *args, **kwargs):
    #     self.status = "Working"
    #     super(Batch, self).save(*args, **kwargs)

    @cached_property
    def totals(self):
        totals = 0
        for f in self.card_batch.all():
            totals += f.price
        return totals or 0


class CouponCard(models.Model):

    Status_Choices = (
        ("Sold", "Sold"),
        ("Working", "Working"),
    )
    batch = models.ForeignKey(
        Batch,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="card_batch",
    )
    serial = models.CharField(max_length=30, null=True, blank=True, unique=True)
    expiry_date = models.DateField(null=True, blank=True)
    seller = models.ForeignKey(
        Users, null=True, blank=True, on_delete=models.CASCADE, related_name="card_user"
    )
    cvv = models.CharField(max_length=6, null=True, blank=True)
    sold = models.BooleanField(default=False)
    in_my_cart = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.serial)[0:6] + ": " + str(self.seller.username)

    class Meta(object):
        verbose_name = "Coupon Card"
        verbose_name_plural = "Coupon Card"
        abstract = False
        db_table = "Coupon Card"

    @cached_property
    def batch_card(self):
        cards = Batch.objects.filter(name=self.batch.name)
        for card in cards:
            return card

    @cached_property
    def country(self):
        country = Country.objects.filter(code=str(self.serial)[0:6])
        country_name = ""
        for c in country:
            country_name += c.name
        return str(country_name) or 'Unknown'

    @cached_property
    def code(self):
        country = Country.objects.filter(code=str(self.serial)[0:6])
        country_code = ""
        for c in country:
            country_code += c.code
        return str(country_code)

    @cached_property
    def card_first_chars(self):
        return str(self.serial)[0:6] + "****"

    @cached_property
    def price(self):
        if self.country == "UNITED STATES":
            price = 5
        elif self.country != "UNITED STATES" and self.country != None:
            price = 10
        else:
            price = 7

        return price

    # @cached_property
    # def batch_total_price(self):
    #     fg = CouponCard.objects.select_related("batch")
    #     total = 0
    #     for f in fg:
    #         total=+ f.price
    #         print(f.price)
    #     return total

    @cached_property
    def card_status(self):
        status = Payout.objects.filter(user=self.seller)

        for stat in status:
            status = stat.status
        return status or None

    @cached_property
    def card_type(self):
        card_type = ""
        if str(self.serial)[0:1] == str(3):
            card_type = "Americarn Express"
        elif str(self.serial)[0:1] == str(4):
            card_type = "Visa"
        elif str(self.serial)[0:1] == str(5):
            card_type = "Master Card"
        elif str(self.serial)[0:1] == str(6):
            card_type = "Discover"
        else:
            card_type = " "
        return str(card_type)
