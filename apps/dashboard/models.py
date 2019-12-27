from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('właściciel'), on_delete=models.PROTECT, related_name='organizations')
    name = models.CharField(verbose_name=_('nazwa organizacji'), max_length=50)
    description = models.TextField(verbose_name=_('opis organizacji'), max_length=1000, null=True, blank=True)
    location = models.CharField(verbose_name=_('lokalizacja / miasto'), max_length=50, null=True, blank=True)
    private = models.BooleanField(verbose_name=_('organizacja prywatna'), default=False)

    def get_main_club_categories(self):
        return self.club_categories.filter(parent=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('organizacja')
        verbose_name_plural = _('organizacje')


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)
    native_name = models.CharField(max_length=128)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Season(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT, related_name='seasons')
    name = models.CharField(verbose_name=_('nazwa sezonu'), max_length=50)
    start_year = models.IntegerField(verbose_name=_('rok rozpoczęcia'))
    double_year = models.BooleanField(verbose_name=_('rozgrywki w dwóch latach'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('sezon rozgrywek')
        verbose_name_plural = _('sezony rozgrywek')


class ClubCategory(models.Model):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='club_categories'
    )
    name = models.CharField(verbose_name=_('nazwa kategorii'), max_length=50)
    parent = models.ForeignKey(
        'self', verbose_name=_('kategoria nadrzędna'), null=True, default=None,
        blank=True, on_delete=models.PROTECT, related_name='children'
    )

    def get_children(self):
        return ClubCategory.objects.filter(parent=self)

    def distance_to_root(self):
        category = self
        distance = 0
        while category.parent is not None:
            distance += 1
            category = category.parent
        return distance

    def distance_to_farthest_leaf(self):
        qs = ClubCategory.objects.filter(parent=self)
        if qs.exists():
            return self.__distance_to_farthest_leaf_recurs(qs)
        return 0

    def __distance_to_farthest_leaf_recurs(self, queryset):
        counter = 1
        for field in queryset:
            qs = ClubCategory.objects.filter(parent=field)
            if qs.exists():
                counter += self.__distance_to_farthest_leaf_recurs(qs)
        return counter

    def am_i_in_myself(self, myself):
        category = self
        while category.parent is not None:
            if category.parent == myself:
                return True
            category = category.parent
        return False

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('Edytowana kategoria nie może być swoją kategorią nadrzędną.'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('kategoria klubów')
        verbose_name_plural = _('kategorie klubów')
        unique_together = ['organization', 'parent', 'name']


class Club(models.Model):
    category = models.ForeignKey(ClubCategory, on_delete=models.PROTECT, related_name='clubs')
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT, related_name='clubs')
    name = models.CharField(max_length=50)
    founded = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    national = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
