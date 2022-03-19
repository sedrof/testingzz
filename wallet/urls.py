
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"my-orders", OrdersViewSet, basename="card")
# router.register(r"my-cards", MyCardsViewSet, basename="MyCards")
# router.register(r"my-credit", MyCreditViewSet, basename="MyCredit")

urlpatterns = [
    # path('orders/', update_api ,name='orders'),

    path("", include(router.urls)),


]