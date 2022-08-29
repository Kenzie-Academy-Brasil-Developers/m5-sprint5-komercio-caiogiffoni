from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class IsOwner(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: User
    ) -> bool:
        print(obj)
        print(obj.id)
        print(request.user)
        print(request.user.id)
        return request.user and request.user.id == obj.id
