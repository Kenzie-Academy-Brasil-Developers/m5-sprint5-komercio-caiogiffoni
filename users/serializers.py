from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already exists"
            )
        ],
    )
    is_seller = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserIdSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]


class UserPatchSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser",
        ]

class UserPatchAdminSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        ]
        read_only_fields = [
            "date_joined",
            "is_superuser",
        ]
