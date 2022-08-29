from rest_framework import status
from rest_framework.response import Response


class CreateByMethodMixin:
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)
