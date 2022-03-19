from sellers.models import Users

from rest_framework import serializers
from orders.models import Orders, Credit
from cards.models import *


class OrdersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Orders
        fields = "__all__"


class CardsSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = CouponCard
        fields = (
            "id",
            "seller",
            "expiry_date",
            "serial",
            "country",
            "cvv",
            "price",
            "card_type",
        )

    def to_representation(self, instance):
        rep = super(CardsSerializer, self).to_representation(instance)
        rep["seller"] = instance.seller.username
        return rep


class CreditSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Credit
        fields = "__all__"
