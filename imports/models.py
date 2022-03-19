from django.db import models
from cards.models import Country


class Batch(models.Model):
    country_code = models.CharField(max_length=50, null=True, blank=True)
    countr_name = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)


    class Meta:
        verbose_name = "Import"
        verbose_name_plural = "Import"

    def __str__(self):
        return str(self.serial)[0:6] + ": " + str(self.seller.username)

    def save(self, *args, **kwargs):
        self.message = ""

        if self.country_code and self.countr_name:
            country, created = Country.objects.update_or_create(
                code = self.country_code,
                defaults={
                    "name": self.country_name
                }
            )
            country.save()
            self.message += str(country.code) + ' ' + str(country.name) + '\n'
        else:
            self.message += 'There was an error in the input fields.'


        super(Batch, self).save(*args, **kwargs)