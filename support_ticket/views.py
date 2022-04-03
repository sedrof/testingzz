from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import TicketCreateForm, TicketEditForm, PostForm
from django.contrib.auth.decorators import user_passes_test, login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from wallet.models import *
from orders.models import Credit
from .serializers import *
from .models import Ticket
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here..


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = "page_size"
    max_page_size = 20


@user_passes_test(lambda u: u.is_superuser)
def all_tickets_view(request):
    user = request.user
    if "q" in request.GET and request.GET.get("q"):
        q = request.GET.get("q")
        tickets_open = Ticket.objects.filter(created_by__username__icontains=q)
        ticket_paginator = Paginator(tickets_open, 200)
    else:
        tickets_open = Ticket.objects.all()
        ticket_paginator = Paginator(tickets_open, 20)

    page_num = request.GET.get("page")
    page = ticket_paginator.get_page(page_num)

    return render(request, "tickets/all-tickets.html", {"page": page})


@login_required
def my_tickets(request):
    user = request.user

    tickets_open = Ticket.objects.filter(created_by=user)

    return render(request, "tickets/my-tickets.html", {"tickets": tickets_open})


@login_required
def ticket_create_view(request):

    if request.POST:
        form = TicketCreateForm(request.POST)

        if form.is_valid():

            obj = form.save()
            # set owner
            obj.created_by = request.user
            obj.status = "IN PROGRESS"
            obj.save()

            messages.add_message(
                request, messages.SUCCESS, "Ticket created successfully"
            )

            if request.user.is_superuser:
                return redirect("all-tickets")
            else:
                return redirect("my-tickets")

    else:
        form = TicketCreateForm()

    return render(
        request,
        "tickets/ticket_edit.html",
        {
            "form": form,
        },
    )


# @user_passes_test(lambda u: u.is_superuser)
def ticket_edit_view(request, pk):

    data = Ticket.objects.filter(pk=pk)

    if request.POST:
        form = TicketEditForm(request.POST, instance=data.first())
        if form.is_valid():
            # set field closed_date to now() if status changed to "DONE"
            for d in data:

                if d.status == "Closed":
                    d.status = "IN PROGRESS"
                    d.closed_date = None
                    d.save()
                    break
                if (
                    (d.status == None)
                    or (d.status == "IN PROGRESS")
                    and (d.requested_amount or 0 > 0)
                ):
                    d.status = "Closed"
                    d.closed_date = timezone.now()
                    d.save()
                    credit = Credit.objects.filter(owner=d.created_by).first()
                    print(credit, "creeeeeeeee")
                    credit.credit += d.requested_amount
                    credit.save()
                if d.status == None or d.status == "IN PROGRESS":
                    print(d.requested_amount)
                    d.status = "Closed"
                    d.closed_date = timezone.now()
                    d.save()
                    break

            messages.add_message(request, messages.SUCCESS, "Ticket update success")
            return redirect("all-tickets")

    else:
        form = TicketEditForm(instance=data)

    return render(
        request,
        "tickets/ticket_edit.html",
        {
            "form": form,
        },
    )


# def ticket_reply_view(request, pk):

#     data = Ticket.objects.filter(pk=pk)
#     message_reply = []
#     for r in data.ticket.all():
#         message_reply.append(r.message)
#     print(message_reply)

#     if request.POST:
#         form = PostForm(request.POST, instance=data.first())
#         if form.is_valid():
#             # set field closed_date to now() if status changed to "DONE"
#             for d in data:

#                 if d.status == "Closed":
#                     d.status = "IN PROGRESS"
#                     d.closed_date = None
#                     d.save()
#                     break
#                 if (
#                     (d.status == None)
#                     or (d.status == "IN PROGRESS")
#                     and (d.requested_amount > 0)
#                 ):
#                     d.status = "Closed"
#                     d.closed_date = timezone.now()
#                     d.save()
#                     credit = Credit.objects.filter(owner=d.created_by).first()
#                     credit.credit += d.requested_amount
#                     credit.save()
#                 if d.status == None or d.status == "IN PROGRESS":
#                     print(d.requested_amount)
#                     d.status = "Closed"
#                     d.closed_date = timezone.now()
#                     d.save()
#                     break

#             messages.add_message(request, messages.SUCCESS, "Ticket update success")
#             return redirect("all-tickets")

#     else:
#         form = TicketEditForm(instance=data)

#     return render(
#         request,
#         "tickets/ticket_edit.html",
#         {
#             "form": form,
#         },
#     )


@user_passes_test(lambda u: u.is_superuser)
def ticket_edit_all(request):

    data = Ticket.objects.all()
    print(data)
    if data:
        for f in data:
            f.status = "Closed"
            f.closed_date = timezone.now()
            f.save()
        messages.add_message(request, messages.SUCCESS, "Tickets update success")
        return redirect("all-tickets")

    return render(
        request,
        "tickets/all-tickets.html",
        {},
    )


# @user_passes_test(lambda u: u.is_superuser)
def ticket_detail_view(request, pk):

    ticket = Ticket.objects.get(id=pk)
    form = PostForm(request.POST, instance=ticket)
    message_reply = []
    for r in ticket.ticket.all():
        # message_reply.append(r.message)
        print(r.message)
        break
    # print(message_reply, ' yyyyyyy')

    return render(
        request, "tickets/ticket_detail.html", {"ticket": ticket, "form": form}
    )


@api_view(
    [
        "POST",
    ]
)
def request_credit(request):
    user = request.user
    print(request.data)
    requested_amount = request.data["values"]["Amount"]
    if requested_amount:
        wallet = Wallet.objects.filter(status=True).first()
        user_payment_ticket = Ticket.objects.create(
            created_by=user,
            title="Deposite Request",
            description=f'Address: "{wallet.address}"',
            requested_amount=requested_amount,
        ).save()
        return Response({"status": status.HTTP_200_OK})
    else:
        return Response({"status": status.HTTP_400_BAD_REQUEST})


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["serial"]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(created_by__username=self.request.user)


@api_view(
    [
        "PUT",
    ]
)
def add_ticket(request):
    ticket_data = request.data
    print(ticket_data, "tickets")
    title = ticket_data["title"]
    description = ticket_data["description"]
    create = Ticket.objects.create(description=description, title=title, created_by=request.user)
    create.save()
    return Response({"status": status.HTTP_200_OK})
@api_view(
    [
        "PUT",
    ]
)
def delete_ticket(request):
    ticket_data = request.data
    print(ticket_data, "tickets")
    ticket = Ticket.objects.get(id=ticket_data['card_ids']).delete()
    return Response({"status": status.HTTP_200_OK})

@api_view(
    [
        "PUT",
    ]
)
def add_reply(request):
    ticket_data = request.data
    print(ticket_data, "tickets")
    ticket = Ticket.objects.get(id=ticket_data['id'])
    reply = Reply.objects.create(ticket=ticket, message=ticket_data['reply'], created_by=request.user)
    reply.save()
    # title = ticket_data["title"]
    # description = ticket_data["description"]
    # create = Reply.objects.create(description=description, title=title, created_by=request.user)
    # create.save()
    return Response({"status": status.HTTP_200_OK})
