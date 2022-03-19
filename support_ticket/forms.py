from django import forms
from .models import Ticket, Reply


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description")


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("status",)


class PostForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['message',]