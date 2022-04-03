from django import forms
from .models import Ticket, Reply


class TicketCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = True
        self.fields["description"].required = True

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
        fields = [
            "message",
        ]
