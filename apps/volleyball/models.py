from django.db import models

from apps.dashboard.models import (
    CategoryNestedModel,
    GameCategory,
    Organization,
    Season,
    Team,
)


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
