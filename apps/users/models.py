from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.dashboard.models import Country


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    default_country = models.ForeignKey(Country, null=True, on_delete=models.PROTECT)
