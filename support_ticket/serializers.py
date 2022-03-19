
from rest_framework import serializers
from .models import *


class TicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"