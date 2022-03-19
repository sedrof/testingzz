from django.db import models
from django.conf import settings
from django.utils.text import Truncator
# Create your models here.


class Ticket(models.Model):

    title = models.CharField("Title", max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owner",
        blank=True,
        null=True,
        verbose_name="created_by",
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        "Description", blank=True, null=True, max_length=1000
    )

    STATUS_CHOICES = (
        ("IN PROGRESS", "IN PROGRESS"),
        ("Closed", "Closed"),
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=250,
        blank=True,
        null=True,
        default="IN PROGRESS",
    )

    # set in view when status changed to "DONE"
    closed_date = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    requested_amount = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return str(self.id)


class Reply(models.Model):

    message  = models.TextField(max_length=4000)
    ticket = models.ForeignKey(Ticket, related_name="ticket", null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reply_user",
        blank=True,
        null=True,
        verbose_name="created_by",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        truncted_message = Truncator(self.message)
        return truncted_message.chars(30)