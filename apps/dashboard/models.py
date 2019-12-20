from django.conf import settings
from django.db import models


class Organization(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='organizations')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    private = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)
    native_name = models.CharField(max_length=128)
    code = models.CharField(max_length=3)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Season(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='seasons')
    name = models.CharField(max_length=30)
    start_year = models.IntegerField()
    double_year = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClubCategory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='club_categories')
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Club(models.Model):
    category = models.ForeignKey(ClubCategory, on_delete=models.PROTECT, related_name='clubs')
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT, related_name='clubs')
    name = models.CharField(max_length=40)
    founded = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    national = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
