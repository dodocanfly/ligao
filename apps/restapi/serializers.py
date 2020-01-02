from apps.dashboard.models import (
    # GameCategory,
    Season,
    Team,
)
from rest_framework import serializers


# class GameCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GameCategory
#         fields = ('id', 'name', 'parent')


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'name')


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
