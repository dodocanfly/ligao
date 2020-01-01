from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('właściciel'),
        on_delete=models.PROTECT, related_name='organizations'
    )
    name = models.CharField(verbose_name=_('nazwa organizacji'), max_length=50)
    description = models.TextField(verbose_name=_('opis organizacji'), max_length=1000, null=True, blank=True)
    location = models.CharField(verbose_name=_('lokalizacja / miasto'), max_length=50, null=True, blank=True)
    private = models.BooleanField(verbose_name=_('organizacja prywatna'), default=False)

    def get_main_club_categories(self):
        return self.club_categories.filter(parent=None).order_by('name')

    def get_main_team_categories(self):
        return self.team_categories.filter(parent=None).order_by('name')

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
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='seasons'
    )
    name = models.CharField(verbose_name=_('nazwa sezonu'), max_length=50)
    start_year = models.IntegerField(verbose_name=_('rok rozpoczęcia'))
    double_year = models.BooleanField(verbose_name=_('rozgrywki w dwóch latach'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('sezon rozgrywek')
        verbose_name_plural = _('sezony rozgrywek')


class CategoryNestedModel(models.Model):
    name = models.CharField(verbose_name=_('nazwa kategorii'), max_length=50)
    parent = models.ForeignKey(
        'self', verbose_name=_('kategoria nadrzędna'), null=True, default=None,
        blank=True, on_delete=models.PROTECT, related_name='children'
    )

    @classmethod
    def get_objects(cls, parent):
        return cls.objects.filter(parent=parent).order_by('name')

    # method must be overridden in the inherited class
    @staticmethod
    def related_items_exists(category):
        # return category.related_field_name.filter(category=category).exists()
        pass

    def has_items(self):
        def inner_checker(queryset):
            if queryset.exists():
                for field in queryset:
                    if field.related_items_exists(field) or inner_checker(self.get_objects(field)):
                        return True
            return False
        return self.related_items_exists(self) or inner_checker(self.get_objects(self))

    def get_children(self):
        return self.get_objects(self)

    def distance_to_root(self):
        category = self
        distance = 0
        while category.parent is not None:
            distance += 1
            category = category.parent
        return distance

    def distance_to_farthest_leaf(self):
        def inner_counter(queryset, counter=0):
            if queryset.exists():
                counter += 1
                level_counter = 0
                for field in queryset:
                    qs = self.get_objects(field)
                    sub_counter = inner_counter(qs, counter)
                    level_counter = sub_counter if sub_counter > counter else level_counter
                counter = level_counter if level_counter > counter else counter
            return counter
        return inner_counter(self.get_objects(self))

    def am_i_in_myself(self, myself):
        category = self
        if category == myself:
            return True
        while category.parent is not None:
            if category.parent == myself:
                return True
            category = category.parent
        return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ['organization', 'parent', 'name']
        abstract = True


class ClubCategory(CategoryNestedModel):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='club_categories'
    )

    @staticmethod
    def related_items_exists(category):
        return category.clubs.filter(category=category).exists()

    def get_clubs(self):
        return self.clubs.filter(category=self)

    class Meta:
        verbose_name = _('kategoria klubów')
        verbose_name_plural = _('kategorie klubów')


class Club(models.Model):
    category = models.ForeignKey(
        ClubCategory, verbose_name=_('kategoria'), on_delete=models.PROTECT,
        related_name='clubs'
    )
    country = models.ForeignKey(
        Country, verbose_name=_('kraj'), null=True, blank=True,
        on_delete=models.PROTECT, related_name='clubs'
    )
    name = models.CharField(max_length=50, verbose_name=_('nazwa klubu'))
    founded = models.IntegerField(null=True, blank=True, verbose_name=_('rok założenia'))
    description = models.TextField(null=True, blank=True, verbose_name=_('opis'))
    national = models.BooleanField(default=False, verbose_name=_('reprezentacja kraju'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TeamCategory(CategoryNestedModel):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='team_categories'
    )

    @staticmethod
    def related_items_exists(category):
        return category.teams.filter(category=category).exists()

    def get_teams(self):
        return self.teams.filter(category=self)

    class Meta:
        verbose_name = _('kategoria zespołów')
        verbose_name_plural = _('kategorie zespołów')


class Team(models.Model):
    category = models.ForeignKey(
        TeamCategory, verbose_name=_('kategoria'), on_delete=models.PROTECT,
        related_name='teams'
    )
    season = models.ForeignKey(Season, verbose_name=_('sezon'), on_delete=models.PROTECT, related_name='teams')
    club = models.ForeignKey(Club, verbose_name=_('klub'), on_delete=models.PROTECT, related_name='teams')
    name = models.CharField(max_length=50, verbose_name=_('pełna nazwa zespołu'))
    short_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=_('krótka nazwa zespołu'))
    description = models.TextField(null=True, blank=True, verbose_name=_('opis'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
