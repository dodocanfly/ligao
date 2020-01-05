from django.shortcuts import render
from django.urls import reverse_lazy

from apps.dashboard.models import Organization
from apps.dashboard.views import (
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)
from .forms import GameAddEditForm
from .models import Game

"""
##############################################################################
                                 GAMES VIEWS
##############################################################################
"""


class GameListView(BaseListView):
    template_name = 'volleyball/game-list.html'

    def get_queryset(self):
        return Organization.get_all_with_games(self.request.user)


class GameAddView(BaseCreateView):
    form_class = GameAddEditForm
    template_name = 'volleyball/game-add.html'
    success_url = reverse_lazy('game-list')


class GameEditView(BaseUpdateView):
    model = Game
    form_class = GameAddEditForm
    template_name = 'volleyball/game-edit.html'
    success_url = reverse_lazy('game-list')


class GameDeleteView(BaseDeleteView):
    model = Game
    template_name = 'volleyball/game-delete.html'
    success_url = reverse_lazy('game-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Game.objects.filter(id=obj.id, category__organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj
