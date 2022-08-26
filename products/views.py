from django.shortcuts import render
from rest_framework import authentication, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products import serializers
from products.mixins import CreateByMethodMixin, SerializerByMethodMixin
from products.models import Product
from products.serializers import ProductDetailFilterSerializer, ProductDetailSerializer, ProductSerializer

# Create your views here.


class ProductsView(
    CreateByMethodMixin,
    SerializerByMethodMixin,
    generics.ListCreateAPIView,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }


class ProductsDetailView(SerializerByMethodMixin,generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductDetailFilterSerializer,
        "PATCH": ProductDetailSerializer,
    }
