
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"cards_seller", CardsViewSet, basename="card")
router.register(r"cards_serial", Cards_SerialViewSet, basename="card")
router.register(r"cards_price", Cards_PriceViewSet, basename="card")
router.register(r"cards_country", Cards_CountryViewSet, basename="card")

urlpatterns = [
    path('all-cards/', all_cards_view,name='all_cards'),
    path('all-batches/', all_batches_view,name='all_batches'),
    path('batch/<int:pk>/', batch_detail_view,name='batch_detail'),
    path('batch-edit/<int:pk>/', batch_edit_view,name='batch_edit'),
    path('batch-delete/<int:pk>/', batch_delete_view,name='batch_delete'),
    path("", include(router.urls)),


]