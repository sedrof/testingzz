from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth import (
    views as auth_views,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status, filters
from .forms import SignUpForm
from .models import *
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserCreateSerializer
from cards.models import *
from .serializers import *


@login_required
def home(request):
    return render(request, "home.html")


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        ip_address = request.META.get("HTTP_X_REAL_IP")
    else:
        ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


class Login(auth_views.LoginView):
    def post(self, request, *args, **kwargs):
        request_body = self.request.POST
        if not request_body:
            return None
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        recaptcha_token = request_body["g-recaptcha-response"]
        ip_addr = get_client_ip(self.request)
        if not user:
            messages.error(request, " Incorrect Username Or Password")
        if not recaptcha_token:
            messages.error(request, " Incorrect")
            return redirect("login")
        if recaptcha_token and user:
            print(recaptcha_token, " recaaa")
            auth_login(request, user)
            return redirect("home")
        return super().post(self, request, *args, **kwargs)


def change_password(request):
    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("password_change_done")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "authenticate/change_password.html", {"form": form})


@login_required
def create_seller(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(request.POST)
        if form.is_valid():
            if request.POST["choices"] == "Seller":
                Users.objects.create(
                    username=request.POST["username"],
                    email=request.POST["email"],
                    password=request.POST["password1"],
                    is_staff=True,
                )
                return redirect("home")
            elif request.POST["choices"] == "Admin":
                Users.objects.create(
                    username=request.POST["username"],
                    email=request.POST["email"],
                    password=request.POST["password1"],
                    is_staff=True,
                    is_superuser=True,
                )
                return redirect("home")
            elif request.POST["choices"] == "Buyer":
                Users.objects.create(
                    username=request.POST["username"],
                    email=request.POST["email"],
                    password=request.POST["password1"],
                    is_staff=False,
                    is_superuser=False,
                )
                return redirect("home")

    return render(request, "authenticate/create_user.html", {"form": form})


class create_user_api(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request.method == "POST":
            emails = []
            for mail in Users.objects.all():
                emails.append(str(mail.email))
            if request.data["username"] == str(
                Users.objects.filter(username=request.data["username"]).first()
            ):
                print('username taken')
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "reason": "Invalid username, already taken.",
                    }
                )
            elif request.data["email"] in emails:
                print('mail taken')
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "reason": "Invalid email address, already taken.",
                    }
                )
            elif request.data["email"] is None:
                print('username taken')
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "reason": "Invalid email address, already taken.",
                    }
                )
            elif request.data["username"] is None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "reason": "Invalid email address, already taken.",
                    }
                )
            else:
                print('creating normal user')
                Users.objects.create(
                    username=request.data["username"],
                    email=request.data["email"],
                    password=request.data["password1"],
                    is_staff=False,
                    is_superuser=False,
                )

                return Response({"status": status.HTTP_200_OK})
