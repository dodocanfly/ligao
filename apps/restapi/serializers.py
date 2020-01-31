from apps.dashboard.models import (
    # GameCategory,
    ClubCategory,
    TeamCategory,
    Season,
    Team,
)
from rest_framework import serializers


# class GameCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GameCategory
#         fields = ('id', 'name', 'parent')


class ClubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubCategory
        fields = ('id', 'name', 'parent')


class TeamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ('id', 'name', 'parent')


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'name')


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
