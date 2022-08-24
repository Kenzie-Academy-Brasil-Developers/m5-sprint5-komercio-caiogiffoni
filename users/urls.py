from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("users/accounts/", views.UserView.as_view()),
    path("login/", auth_view.obtain_auth_token),
]
