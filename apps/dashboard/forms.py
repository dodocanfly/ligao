from django import forms
from django.http import Http404
from django.utils.html import mark_safe

from apps.dashboard.models import Organization, Season, ClubCategory, Club, TeamCategory, Team
from .forms_config import FIELDS_ATTRS
from .validators import valid_am_i_in_myself, valid_max_tree_depth, valid_same_organization, valid_can_change_org


class NestedModelChoiceField(forms.ModelChoiceField):
    indent_spaces_number = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._populate_choices()

    def _prepare_categories(self):
        organizations = {}
        for category in self.queryset:
            if category.organization_id not in organizations:
                organizations[category.organization_id] = {
                    'name': category.organization.name,
                    'cats': {},
                }
            parent_id = 0 if category.parent is None else category.parent_id
            if parent_id not in organizations[category.organization_id]['cats']:
                organizations[category.organization_id]['cats'][parent_id] = {}
            organizations[category.organization_id]['cats'][parent_id][category.id] = category
        return organizations.items()

    def _populate_choices(self):

        def prepare_choices(cats, index, level):
            choices = []
            for cat_id, cat_obj in cats[index].items():
                indend = '&nbsp;' * (self.indent_spaces_number * level)
                choices.append([cat_id, mark_safe(indend + cat_obj.name)])
                if cat_id in cats:
                    choices.extend(prepare_choices(cats, cat_id, level + 1))
            return choices

        self.choices = [['', '----------']]
        for idx, organization in self._prepare_categories():
            self.choices.append([
                organization['name'],
                prepare_choices(organization['cats'], 0, 0),
            ])


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def set_widget_attrs(self):
        model_key = self.__class__.__name__
        if model_key in FIELDS_ATTRS:
            for field, attrs in FIELDS_ATTRS[model_key].items():
                if field in self.fields:
                    self.fields[field].widget.attrs = attrs


class OrganizationAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Organization.objects.filter(id=self.initial.get('id'), owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.set_widget_attrs()

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.owner = self.request.user
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        exclude = ['owner']


class SeasonAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Season.objects.filter(id=self.initial.get('id'), organization__owner=self.request.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.request.user)
        self.set_widget_attrs()

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
        self.set_widget_attrs()

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
        )
        if not self.initial and self.request.user.default_country:
            self.fields['country'].initial = self.request.user.default_country.id
        self.set_widget_attrs()

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
        self.set_widget_attrs()

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
        )
        self.fields['season'].queryset = Season.objects.filter(organization__owner=self.request.user).order_by('name')
        self.fields['club'].queryset = Club.objects.filter(category__organization__owner=self.request.user).order_by('name')
        self.set_widget_attrs()

    class Meta:
        model = Team
        fields = ('id', 'category', 'season', 'club', 'name', 'short_name', 'description')
