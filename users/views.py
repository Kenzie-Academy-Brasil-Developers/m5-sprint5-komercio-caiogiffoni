from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from users.models import User
from users.serializers import UserSerializer

# Create your views here.


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserNewestView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def get_queryset(self):
      num = self.kwargs["num"]
      return self.queryset.order_by("-date_joined")[0:num]
      
