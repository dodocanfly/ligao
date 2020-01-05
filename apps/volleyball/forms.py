from django import forms
from django.http import Http404

from .forms_config import FIELDS_ATTRS
from .models import Game
from apps.dashboard.models import Organization, Season, ClubCategory, Club, TeamCategory, Team, GameCategory
from apps.dashboard.forms import MyModelForm, NestedModelChoiceField
from apps.dashboard.validators import valid_cat_is_leaf


class GameAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Game.objects.filter(id=self.initial.get('id'), category__organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['category'] = NestedModelChoiceField(
            queryset=GameCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[valid_cat_is_leaf],
        )
        self.fields['season'].queryset = Season.objects.filter(organization__owner=self.request.user).order_by('name')
        self.fields['teams'].widget = forms.SelectMultiple()
        self.fields['teams'].queryset = Team.objects.filter(category__organization__owner=self.request.user).order_by('name')
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = Game
        fields = ('id', 'category', 'season', 'teams', 'name', 'up_to_sets', 'scoring_system')
