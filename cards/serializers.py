from rest_framework import serializers

from cards.models import *



class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponCard
        fields = ('id','seller', 'country', 'card_first_chars', 'price', 'card_type', 'sold' )

    def to_representation(self, instance):
        rep = super(CardsSerializer, self).to_representation(instance)
        rep['seller'] = instance.seller.username
        return rep