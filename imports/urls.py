from django.urls import path
from .views import *

urlpatterns = [
    path('', model_form_upload,name='imports'),
    path('cards/', model_form_upload_cards,name='imports_cards'),
]