from django.urls import path
from .views import *

urlpatterns = [
    path('new/', payout_create_view,name='payout_new'),
    path('payout-user/', all_payouts_view,name='all_payouts'),
    path('payout-user-edit/<int:pk>/', payout_edit_view,name='payouts_edit'),

]