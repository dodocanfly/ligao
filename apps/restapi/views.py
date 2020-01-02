from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import User

from apps.dashboard.models import (
    # GameCategory,
    Season,
    Team,
)
from apps.restapi.serializers import (
    # GameCategorySerializer,
    SeasonSerializer,
    TeamsSerializer,
)


# class GameCategoryViewSet(ModelViewSet):
#     queryset = GameCategory.objects.all()
#     serializer_class = GameCategorySerializer
#
#     def get_queryset(self):
#         organization = self.request.query_params.get('organization')
#         if organization and organization.isnumeric():
#             return GameCategory.objects.filter(organization__owner=self.request.user, organization_id=int(organization))


class SeasonViewSet(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    def get_queryset(self):
        organization = self.request.query_params.get('organization')
        if organization and organization.isnumeric():
            return Season.objects.filter(organization__owner=self.request.user, organization_id=int(organization))


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamsSerializer

    def get_queryset(self):
        season = self.request.query_params.get('season')
        game = self.request.query_params.get('game')
        if season and season.isnumeric():
            return Team.objects.filter(season__organization__owner=self.request.user, season_id=int(season))
        if game and game.isnumeric():
            return Team.objects.filter(games__organization__owner=self.request.user, games__exact=int(game))


class GameDataView(APIView):
    def get(self, request, id=0):
        usernames = {
            'lastround': 5,
            'lastpos': 3,
        }
        return Response(usernames)
