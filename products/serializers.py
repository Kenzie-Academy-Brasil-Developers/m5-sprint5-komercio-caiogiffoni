from rest_framework import serializers
from users.serializers import UserIdSerializer

from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserIdSerializer(read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )
    quantity = serializers.IntegerField(min_value=0)

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
