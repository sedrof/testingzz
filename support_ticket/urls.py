
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"user-tickets", TicketsViewSet, basename="ticket")

urlpatterns = [
    path('new/', ticket_create_view,name='ticket_new'),
    path('all-tickets/', all_tickets_view,name='all-tickets'),
    path('request-credit/', request_credit,name='request_credit'),
    path('add-ticket/', add_ticket,name='add_ticket'),
    path('add-reply/', add_reply,name='add_reply'),
    path('delete-tickets/', delete_ticket,name='delete_ticket'),
    path('my-tickets/', my_tickets,name='my-tickets'),
    path('ticket/<int:pk>/', ticket_detail_view,name='ticket_detail'),
    path('ticket/edit/<int:pk>/', ticket_edit_view,name='ticket_edit'),
    # path('ticket/reply/<int:pk>/', ticket_reply_view,name='ticket_reply'),
    path('ticket/edit-all/', ticket_edit_all,name='ticket_edit_all'),
    path("", include(router.urls)),


]