from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from users.models import User
from users.permissions import IsOwner
from users.serializers import (
    UserPatchAdminSerializer,
    UserPatchSerializer,
    UserSerializer,
)

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserNewestView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:num]


class UserDetailView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    queryset = User.objects.all()
    serializer_class = UserPatchSerializer


class UserManagementDetailView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserPatchAdminSerializer
