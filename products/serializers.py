from rest_framework import serializers
from users.serializers import UserIdSerializer

from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserIdSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

        read_only_fields = ["is_active"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]


class ProductDetailFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # exclude = ["id"]
        fields = ["description", "price", "quantity", "is_active", "seller"]

    seller = UserIdSerializer()
