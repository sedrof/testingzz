from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"home", HomeViewSet, basename="home")

urlpatterns = [
    path('', my_home,name='home'),
    path("", include(router.urls)),

]