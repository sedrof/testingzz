from rest_framework import serializers
from .models import *


class homeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'

    # def to_representation(self, instance):
    #     rep = super(RepliesSerializer, self).to_representation(instance)
    #     rep["created_by"] = instance.created_by.username
    #     return rep