from django.urls import path
from rest_framework.authtoken import views as auth_view

from . import views

urlpatterns = [
    path("accounts/", views.UserView.as_view(), name="register"),
    path("accounts/newest/<int:num>/", views.UserNewestView.as_view()),
    path("accounts/<str:pk>/", views.UserDetailView.as_view(), name='filter'),
    path(
        "accounts/<pk>/management/", views.UserManagementDetailView.as_view(), name='filter_patch_admin'
    ),
    path("login/", auth_view.obtain_auth_token, name="login"),
]
