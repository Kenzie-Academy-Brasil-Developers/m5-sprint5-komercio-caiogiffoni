from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    # campos pedidos no TERMINAL com createsuperuser
    REQUIRED_FIELDS = ["first_name", "last_name"]
