from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from products.mixins import CreateByMethodMixin, SerializerByMethodMixin
from products.models import Product
from products.permissions import IsProductSellerOrReadOnly, IsSellerOrReadOnly
from products.serializers import (
    ProductDetailFilterSerializer,
    ProductDetailSerializer,
    ProductSerializer,
)

# Create your views here.


class ProductsView(
    SerializerByMethodMixin, CreateByMethodMixin, generics.ListCreateAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }


class ProductsDetailView(
    SerializerByMethodMixin, generics.RetrieveUpdateAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProductSellerOrReadOnly]

    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductDetailFilterSerializer,
        "PATCH": ProductDetailSerializer,
    }
