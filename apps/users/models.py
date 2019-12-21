from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.dashboard.models import Country


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='adres e-mail', unique=True)
    default_country = models.ForeignKey(Country, verbose_name=_('domyślny kraj'), null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('użytkownik')
        verbose_name_plural = _('użytkownicy')
