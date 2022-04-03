from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from cards.forms import BatchEditForm
from django.contrib import messages
from .models import *
from .serializers import *


@user_passes_test(lambda u: u.is_superuser)
def all_cards_view(request):
    user = request.user

    if "q" in request.GET and request.GET.get("q"):
        q = request.GET.get("q")
        print(type(q))
        cards = CouponCard.objects.filter(seller__username__icontains=q)
        ticket_paginator = Paginator(cards, 200)
    else:
        cards = CouponCard.objects.all()
        ticket_paginator = Paginator(cards, 20)

    page_num = request.GET.get("page")
    page = ticket_paginator.get_page(page_num)
    num_pages = ticket_paginator.num_pages

    return render(
        request, "cards/all_cards.html", {"page": page, "num_pages": num_pages}
    )


@user_passes_test(lambda u: u.is_superuser)
def all_batches_view(request):
    user = request.user

    if "q" in request.GET and request.GET.get("q"):
        q = request.GET.get("q")
        print(type(q))
        batches = Batch.objects.filter(name=q)
        ticket_paginator = Paginator(batches, 200)
    else:
        batches = Batch.objects.all()
        ticket_paginator = Paginator(batches, 20)

    page_num = request.GET.get("page")
    page = ticket_paginator.get_page(page_num)
    num_pages = ticket_paginator.num_pages
    print(num_pages, " nummm")

    return render(
        request, "batch/all_batches.html", {"page": page, "num_pages": num_pages}
    )


@user_passes_test(lambda u: u.is_superuser)
def batch_detail_view(request, pk):
    if "q" in request.GET and request.GET.get("q"):
        q = request.GET.get("q")
        batch = CouponCard.objects.filter(Q(batch__id=pk) & Q(serial__icontains=q))
        ticket_paginator = Paginator(batch, 5)
    else:
        batch = CouponCard.objects.filter(batch__id=pk)
        ticket_paginator = Paginator(batch, 5)

    batch_1 = CouponCard.objects.filter(batch__id=pk).first
    page_num = request.GET.get("page")
    page = ticket_paginator.get_page(page_num)
    num_pages = ticket_paginator.num_pages

    # batch_total_price = [f.totals for f in Batch.objects.filter(id=pk)][0]

    return render(
        request,
        "batch/batch_cards.html",
        {
            "page": page,
            "num_pages": num_pages,
            "batch": batch_1,
            # "batch_total_price": batch_total_price,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def batch_edit_view(request, pk):

    data = Batch.objects.filter(pk=pk)

    if request.POST:
        form = BatchEditForm(request.POST, instance=data.first())
        if form.is_valid():
            # set field closed_date to now() if status changed to "DONE"
            for d in data:

                if d.status == "Stop":
                    print("here")
                    d.status = "Working"
                    d.closed_date = None
                    d.save()
                    break
                if d.status == None or d.status == "Working":
                    print("here none")
                    d.status = "Stop"
                    d.save()
                    break

            messages.add_message(request, messages.SUCCESS, "Batch update success")
            return redirect("all_batches")

    else:
        form = BatchEditForm(instance=data)

    return render(
        request,
        "tickets/ticket_edit.html",
        {
            "": "",
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def batch_delete_view(request, pk):

    data = Batch.objects.filter(pk=pk)

    if request.POST:
        data = Batch.objects.filter(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, "Batch Delete success")
        return redirect("all_batches")

    else:
        form = BatchEditForm(instance=data)

    return render(
        request,
        "tickets/ticket_edit.html",
        {
            "": "",
        },
    )


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20


class CardsViewSet(viewsets.ModelViewSet):
    queryset = CouponCard.objects.filter(batch__status="Working").filter(sold=False)
    serializer_class = CardsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["seller__username"]
    pagination_class = LargeResultsSetPagination

    # def get_queryset(self):
    #     chp = self.request.body
    #     print(chp)
    #     if self.request.user.is_superuser:
    #         return super().get_queryset()
    #     else:
    #         return super().get_queryset().filter(user=self.request.user)


class Cards_SerialViewSet(viewsets.ModelViewSet):
    queryset = CouponCard.objects.filter(batch__status="Working").filter(sold=False)
    serializer_class = CardsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["serial"]
    pagination_class = LargeResultsSetPagination

    # def get_queryset(self):
    #     chp = self.request.body
    #     print(chp)
    #     if self.request.user.is_superuser:
    #         return super().get_queryset()
    #     else:
    #         return super().get_queryset().filter(serial__startswith='0123')


class Cards_PriceViewSet(viewsets.ModelViewSet):
    queryset = CouponCard.objects.filter(batch__status="Working").filter(sold=False)
    serializer_class = CardsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["price"]
    pagination_class = LargeResultsSetPagination


class Cards_CountryViewSet(viewsets.ModelViewSet):
    queryset = CouponCard.objects.filter(batch__status="Working").filter(sold=False)
    serializer_class = CardsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["country"]
    pagination_class = LargeResultsSetPagination

    # def price_func(price):
    #     return price.objects.all()

    # def get_queryset(self):
    #     qs = super(Cards_PriceViewSet, self).get_queryset()
    #     price_search = self.request.GET.get("search", None)
    #     price = []

    #     return qs.filter(price=price_search)

        # if self.request.user.is_superuser:
        #     return super().get_queryset()
        # else:
        #     return super().get_queryset().filter(serial__startswith="1")
