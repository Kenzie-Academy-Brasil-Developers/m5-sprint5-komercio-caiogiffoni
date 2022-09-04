from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.views import Request, View
from users.models import User

from products.models import Product


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_seller
        )


class IsProductSellerOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: Product, product: Product
    ):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.id == product.seller_id
        )
