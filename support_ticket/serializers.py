from rest_framework import serializers
from .models import *


class RepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["id", "message", "created_by", "created_at"]

    def to_representation(self, instance):
        rep = super(RepliesSerializer, self).to_representation(instance)
        rep["created_by"] = instance.created_by.username
        return rep


class TicketsSerializer(serializers.ModelSerializer):
    reply = RepliesSerializer(many=True, source="ticket")

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "created_by",
            "created",
            "description",
            "status",
            "requested_amount",
            "updated",
            "closed_date",
            "reply",
        ]

    def to_representation(self, instance):
        rep = super(TicketsSerializer, self).to_representation(instance)
        rep["created_by"] = instance.created_by.username
        return rep
