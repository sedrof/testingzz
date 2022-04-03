
from re import X
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import *
from .serializers import *
from cards.models import CouponCard
from sellers.models import Users

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = "page_size"
    max_page_size = 20

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["serial"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner__username=self.request.user).filter(sold = False)

    def destroy(self, request, *args, **kwargs):
        trans = self.get_object()
        print(trans.id, "chp")
        return Response(data="delete success")

class MyCardsViewSet(viewsets.ModelViewSet):
    queryset = CouponCard.objects.all()
    serializer_class = CardsSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["serial"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(seller__username=self.request.user)

class MyCreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["serial"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


@api_view(["POST",])
def update_api(request):
    user = request.user
    card_ids = request.data['selectionData']
    print(card_ids, 'cccccccc')
    for i in range(len(card_ids)):
        orders, created = Orders.objects.update_or_create(
            card_id = card_ids[i]['id'],
            defaults={
                "card_first_chars": card_ids[i]["card_first_chars"],
                "price": card_ids[i]["price"],
                "card_type": card_ids[i]["card_type"],
                "country": card_ids[i]["country"],
            },

        )
        orders.save()
        orders.owner.add(user)

    return Response({"status": status.HTTP_200_OK})

@api_view(["POST",])
def remove_from_my_cart(request):
    user = request.user
    card_ids = request.data['card_ids']
    print(card_ids, 'caaaaaaaaaards')
    if card_ids:
        order = Orders.objects.filter(card_id=card_ids).first()
        order.owner.remove(user)
        return Response({"status": status.HTTP_200_OK})
    else:
        return Response({"status": status.HTTP_400_BAD_REQUEST})


@api_view(["POST",])
def add_credit(request):
    user = request.user

    order = Credit.objects.filter(owner=user).first()
    order.owner.remove(user)
    return Response({"status": status.HTTP_200_OK})


@api_view(["POST",])
def make_order(request):
    user = request.user
    cards_credit = request.data['results']
    card_ids = []
    card_prices = []
    for c in cards_credit:
        card_ids.append(c['card_id'])
        card_prices.append(c['price'])

    credit = Credit.objects.filter(owner=user).first()
    if credit:
        total_price = sum(card_prices)
        if credit.credit >= total_price:
            new_balance = credit.credit - total_price
            credit.credit = new_balance
            credit.save()
            for c in card_ids:
                card = CouponCard.objects.filter(id = c).first()
                card_seller = card.seller
                seller_creadit = Credit.objects.filter(owner=card_seller).first()
                seller_creadit.credit += card.price
                seller_creadit.save()
                orders = Orders.objects.filter(card_id = c).first()
                
                card.seller = user
                card.sold = True
                card.save()
                orders.sold = True
                orders.save()
            Response({"status": status.HTTP_200_OK})
        else:
            print("None1")
            return Response({"status": status.HTTP_400_BAD_REQUEST})


    else:
        print("None")
        return Response({"status": status.HTTP_400_BAD_REQUEST})


    # return Response({"status": status.HTTP_200_OK})


