from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("products/", views.ProductsView.as_view()),
    path("products/<str:pk>/", views.ProductsDetailView.as_view()),
]
