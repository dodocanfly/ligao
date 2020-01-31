from django import forms
from django.http import Http404
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from utils.forms import MyModelForm, NestedModelChoiceField
from apps.dashboard.models import Organization, Season, ClubCategory, Club, TeamCategory, Team, GameCategory
from .forms_config import FIELDS_ATTRS
from .validators import (
    valid_am_i_in_myself,
    valid_max_tree_depth,
    valid_same_organization,
    valid_can_change_org,
    valid_cat_is_leaf,
)


class OrganizationAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Organization.objects.filter(id=self.initial.get('id'), owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['owner'].initial = self.request.user
        self.fields['owner'].widget = forms.HiddenInput()
        self.set_widget_attrs(FIELDS_ATTRS)

    def clean(self):
        cleaned_data = super().clean()
        if self.request.user != cleaned_data.get('owner'):
            raise ValidationError(_('Hacker!'))

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.owner = self.request.user
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        fields = ('id', 'owner', 'name', 'description', 'location', 'private')


class SeasonAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Season.objects.filter(id=self.initial.get('id'), organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.request.user)
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = Season
        fields = '__all__'


class ClubCategoryAddEditForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = ClubCategory.objects.filter(id=self.initial.get('id'), organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.request.user)
        self.fields['organization'].validators = [valid_can_change_org(self.instance)]
        if self.request.GET.get('o'):
            self.fields['organization'].initial = self.request.GET.get('o')
        self.fields['parent'] = NestedModelChoiceField(
            queryset=ClubCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[
                valid_am_i_in_myself(self.instance),
                valid_max_tree_depth(self.instance),
                valid_same_organization(self),
            ],
            required=False,
        )
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = ClubCategory
        fields = ('id', 'organization', 'name', 'parent')


class ClubAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Club.objects.filter(id=self.initial.get('id'), category__organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['category'] = NestedModelChoiceField(
            queryset=ClubCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[valid_cat_is_leaf],
        )
        if not self.initial and self.request.user.default_country:
            self.fields['country'].initial = self.request.user.default_country.id
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = Club
        fields = ('id', 'category', 'country', 'name', 'founded', 'description', 'national')


class TeamCategoryAddEditForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = TeamCategory.objects.filter(id=self.initial.get('id'), organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.request.user)
        self.fields['organization'].validators = [valid_can_change_org(self.instance)]
        if self.request.GET.get('o'):
            self.fields['organization'].initial = self.request.GET.get('o')
        self.fields['parent'] = NestedModelChoiceField(
            queryset=TeamCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[
                valid_am_i_in_myself(self.instance),
                valid_max_tree_depth(self.instance),
                valid_same_organization(self),
            ],
            required=False,
        )
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = TeamCategory
        fields = ('id', 'organization', 'name', 'parent')


class TeamAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Team.objects.filter(id=self.initial.get('id'), category__organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['category'] = NestedModelChoiceField(
            queryset=TeamCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[valid_cat_is_leaf],
        )
        self.fields['season'].queryset = Season.objects.filter(organization__owner=self.request.user).order_by('name')
        self.fields['club'].queryset = Club.objects.filter(category__organization__owner=self.request.user).order_by('name')
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = Team
        fields = ('id', 'category', 'season', 'club', 'name', 'short_name', 'description')


class GameCategoryAddEditForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = GameCategory.objects.filter(id=self.initial.get('id'), organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.request.user)
        self.fields['organization'].validators = [valid_can_change_org(self.instance)]
        if self.request.GET.get('o'):
            self.fields['organization'].initial = self.request.GET.get('o')
        self.fields['parent'] = NestedModelChoiceField(
            queryset=GameCategory.objects.filter(organization__owner=self.request.user).order_by('organization__name', 'name'),
            validators=[
                valid_am_i_in_myself(self.instance),
                valid_max_tree_depth(self.instance),
                valid_same_organization(self),
            ],
            required=False,
        )
        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = GameCategory
        fields = ('id', 'organization', 'name', 'parent')


class GameAddForm(forms.Form):
    organization = forms.ModelChoiceField(Organization.objects.none())
    category = forms.ModelChoiceField(GameCategory.objects.none())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.all_for_user(self.request.user)
        self.fields['category'].queryset = GameCategory.objects.filter(organization__owner=self.request.user)
