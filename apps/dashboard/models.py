from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.functions import Concat
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

    @classmethod
    def all_for_user(cls, owner):
        return cls.objects.filter(owner=owner)

    @classmethod
    def one_for_user(cls, owner, organization_id):
        return cls.objects.filter(owner=owner, id__exact=organization_id)

    @classmethod
    def get_all_with_club_categories(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('club_categories')).filter(counter__gt=0)

    @classmethod
    def get_one_with_club_categories(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('club_categories')).filter(counter__gt=0)

    @classmethod
    def get_all_with_team_categories(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('team_categories')).filter(counter__gt=0)

    @classmethod
    def get_one_with_team_categories(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('team_categories')).filter(counter__gt=0)

    @classmethod
    def get_all_with_game_categories(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('game_categories')).filter(counter__gt=0)

    @classmethod
    def get_one_with_game_categories(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('game_categories')).filter(counter__gt=0)

    @classmethod
    def get_all_with_clubs(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('club_categories__clubs')).filter(counter__gt=0)

    @classmethod
    def get_one_with_clubs(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('club_categories__clubs')).filter(counter__gt=0)

    @classmethod
    def get_all_with_teams(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('team_categories__teams')).filter(counter__gt=0)

    @classmethod
    def get_one_with_teams(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('team_categories__teams')).filter(counter__gt=0)

    @classmethod
    def get_all_with_games(cls, owner):
        return cls.all_for_user(owner).annotate(counter=models.Count('game_categories__games')).filter(counter__gt=0)

    @classmethod
    def get_one_with_games(cls, owner, organization_id):
        return cls.one_for_user(owner, organization_id).annotate(counter=models.Count('game_categories__games')).filter(counter__gt=0)

    def get_main_club_categories(self):
        return self.club_categories.filter(parent=None).order_by('name')

    def get_main_club_categories_with_items(self):
        ret_cats = []
        for category in self.get_main_club_categories():
            if category.has_items():
                ret_cats.append(category)
        return ret_cats

    def get_main_team_categories(self):
        return self.team_categories.filter(parent=None).order_by('name')

    def get_main_team_categories_with_items(self):
        ret_cats = []
        for category in self.get_main_team_categories():
            if category.has_items():
                ret_cats.append(category)
        return ret_cats

    def get_main_game_categories(self):
        return self.game_categories.filter(parent=None).order_by('name')

    def get_main_game_categories_with_items(self):
        ret_cats = []
        for category in self.get_main_game_categories():
            if category.has_items():
                ret_cats.append(category)
        return ret_cats

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ('name',)
        verbose_name = _('organizacja')
        verbose_name_plural = _('organizacje')


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)
    native_name = models.CharField(max_length=128)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Season(models.Model):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='seasons'
    )
    name = models.CharField(verbose_name=_('nazwa sezonu'), max_length=50)
    start_year = models.IntegerField(verbose_name=_('rok rozpoczęcia'))
    double_year = models.BooleanField(verbose_name=_('rozgrywki w dwóch latach'), default=True)

    @classmethod
    def all_for_user(cls, user):
        return cls.objects.filter(organization__owner=user).order_by('name')

    @classmethod
    def all_for_game_category(cls, category_id):
        return cls.objects.filter(games__category_id=category_id).order_by('name')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ('name',)
        verbose_name = _('sezon rozgrywek')
        verbose_name_plural = _('sezony rozgrywek')


class CategoryNestedModel(models.Model):
    name = models.CharField(verbose_name=_('nazwa kategorii'), max_length=50)
    parent = models.ForeignKey(
        'self', verbose_name=_('kategoria nadrzędna'), null=True, default=None,
        blank=True, on_delete=models.PROTECT, related_name='children'
    )

    @classmethod
    def get_one(cls, owner, category_id):
        return cls.objects.filter(organization__owner=owner, pk=category_id)

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

    @classmethod
    def get_nested_cats_ids_list(cls, cat_id):
        cats_ids = [cat_id]
        for cat in cls.objects.filter(parent_id=cat_id):
            cats_ids.extend(cls.get_nested_cats_ids_list(cat.id))
        return cats_ids

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('organization', 'parent', 'name')
        ordering = ('name',)
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
        unique_together = ('category', 'name')
        ordering = ('name',)


class TeamCategory(CategoryNestedModel):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='team_categories'
    )

    @staticmethod
    def related_items_exists(category):
        return category.teams.filter(category=category).exists()

    def get_teams(self):
        return self.teams.filter(category=self).order_by('season__name', 'name')

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

    @classmethod
    def get_choices(cls, owner, organization_id=None, category_id=None, season_id=None):
        choices = cls.objects.filter(category__organization__owner=owner)
        if organization_id is not None:
            choices = choices.filter(category__organization_id=organization_id)
        if season_id is not None:
            choices = choices.filter(season_id=season_id)
        if category_id is not None:
            choices = choices.filter(category_id__in=TeamCategory.get_nested_cats_ids_list(category_id))

        return choices.order_by('category__name', 'season__start_year', 'season__name', 'name')

    def __str__(self):
        # return self.name
        return '[' + self.category.name + '] ' + '[' + self.season.name + '] ' + self.name

    class Meta:
        unique_together = ('category', 'season', 'name')
        ordering = ('name',)


class GameCategory(CategoryNestedModel):
    organization = models.ForeignKey(
        Organization, verbose_name=_('organizacja'), on_delete=models.PROTECT,
        related_name='game_categories'
    )

    @staticmethod
    def related_items_exists(category):
        return category.games.filter(category=category).exists()

    def get_games(self):
        return self.games.filter(category=self)

    class Meta:
        verbose_name = _('kategoria rozgrywek')
        verbose_name_plural = _('kategorie rozgrywek')


class ScoringSystem(models.Model):
    GAME_UP_TO_SETS_CHOICES = (
        (2, 2),
        (3, 3),
    )
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='volleyball_scoring_systems')
    game_up_to = models.SmallIntegerField(default=3, choices=GAME_UP_TO_SETS_CHOICES)
    name = models.CharField(max_length=50)
    result_3_0 = models.SmallIntegerField(default=0, blank=True)
    result_3_1 = models.SmallIntegerField(default=0, blank=True)
    result_3_2 = models.SmallIntegerField(default=0, blank=True)
    result_2_3 = models.SmallIntegerField(default=0, blank=True)
    result_1_3 = models.SmallIntegerField(default=0, blank=True)
    result_0_3 = models.SmallIntegerField(default=0, blank=True)
    result_2_0 = models.SmallIntegerField(default=0, blank=True)
    result_2_1 = models.SmallIntegerField(default=0, blank=True)
    result_1_2 = models.SmallIntegerField(default=0, blank=True)
    result_0_2 = models.SmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    UP_TO_SETS_CHOICES = (
        (2, 2),
        (3, 3),
    )

    category = models.ForeignKey(GameCategory, related_name='games', on_delete=models.PROTECT)
    season = models.ForeignKey(Season, related_name='games', on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name='games')
    up_to_sets = models.SmallIntegerField(choices=UP_TO_SETS_CHOICES, verbose_name='do ilu setów')
    scoring_system = models.ForeignKey(ScoringSystem, null=True, default=None, on_delete=models.PROTECT, related_name='games')

    def __str__(self):
        return self.name


class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    round = models.SmallIntegerField()
    host_team = models.ForeignKey(Team, related_name='host_team', on_delete=models.PROTECT)
    guest_team = models.ForeignKey(Team, related_name='guest_team', on_delete=models.PROTECT)
    host_sets = models.SmallIntegerField()
    guest_sets = models.SmallIntegerField()
    set_1_host = models.SmallIntegerField()
    set_1_guest = models.SmallIntegerField()
    set_2_host = models.SmallIntegerField()
    set_2_guest = models.SmallIntegerField()
    set_3_host = models.SmallIntegerField(null=True, blank=True)
    set_3_guest = models.SmallIntegerField(null=True, blank=True)
    set_4_host = models.SmallIntegerField(null=True, blank=True)
    set_4_guest = models.SmallIntegerField(null=True, blank=True)
    set_5_host = models.SmallIntegerField(null=True, blank=True)
    set_5_guest = models.SmallIntegerField(null=True, blank=True)
    datetime = models.DateTimeField()
    order = models.SmallIntegerField()
    finished = models.BooleanField(default=False)
    walkover = models.BooleanField(default=False)

    class Meta:
        ordering = ['round', 'order']

    def __str__(self):
        return self.host_team.name + ' - ' + self.guest_team.name
