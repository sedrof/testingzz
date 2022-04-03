from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from homez.models import Home
from .serializers import *

# Create your views here.


@login_required
def my_home(request):
    body = Home.objects.filter(title="Sellers")
    print(body)
    return render(request, "home.html", {"body": body})


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = homeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(title="Buyers")
