from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from apps.dashboard.models import Country


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, verbose_name='adres e-mail', unique=True)
    default_country = models.ForeignKey(Country, verbose_name=_('domyślny kraj'), null=True, blank=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('użytkownik')
        verbose_name_plural = _('użytkownicy')
