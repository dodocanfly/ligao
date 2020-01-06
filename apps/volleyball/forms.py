from django import forms
from django.http import Http404

from .forms_config import FIELDS_ATTRS
from .models import Game
from apps.dashboard.models import Season, Team, GameCategory
from apps.dashboard.validators import valid_cat_is_leaf

from django.utils.html import mark_safe
from django.forms import widgets


TEST_CHOICES = (
    (1, '1'*4, 1, True),
    (2, '2'*4, 2, True),
    (3, '3'*4, 2, True),
    (4, '4'*4, 2, True),
    (5, '5'*4, 2, True),
    (6, '6' * 4, 2, True),
    (7, '7' * 4, 2, True),
    (8, '8' * 4, 2, True),
    (9, '9' * 4, 2, True),
    (10, '10' * 2, 2, True),
)

TEST_CHOICES = [
    (
        "Group 1",
        [
            (1, "Choice 1", 666),
            (2, "Choice 2", 444),
        ],
    ),
    (
        "Group 2",
        [
            (3, "Choice 3", 666),
            (4, "Choice 4", 444),
        ],
    ),
    (5, "Choice 5", 666),
]





class NestedModelChoiceField(forms.ModelChoiceField):
    indent_spaces_number = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_label = None
        self.widget = NestedSelect()
        # self.widget = NestedSelectMultiple()
        self._populate_choices()
        # self.choices = TEST_CHOICES

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

        mychoices = [['', '----------']]
        for idx, organization in self._prepare_categories():
            # self.choices.append([
            #     organization['name'],
            #     prepare_choices(organization['cats'], 0, 0),
            # ])
            mychoices += prepare_choices(organization['cats'], 0, 0)
        self.choices = mychoices

dictitems = (
    [
        (
            5, {
                'name': 'WMZPS',
                'cats': {
                    13: {
                        11: '<GameCategory: III liga mężczyzn>'
                    },
                    14: {
                        12: '<GameCategory: młodziczki>'
                    },
                    0: {
                        14: '<GameCategory: młodzieżowe>',
                        13: '<GameCategory: seniorskie>'
                    }
                }
            }
        )
    ]
)

t = [
    [
        'WMZPS',
        [
            [14, 'młodzieżowe'],
            [12, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;młodziczki'],
            [13, 'seniorskie'],
            [11, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;III liga mężczyzn']
        ]
    ]
]


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def set_widget_attrs(self, source=None):
        if source is None:
            source = FIELDS_ATTRS
        model_key = self.__class__.__name__
        if model_key in source:
            for field, attrs in source[model_key].items():
                if field in self.fields:
                    self.fields[field].widget.attrs = attrs


class NestedSelect(widgets.Select):
    def __init__(self):
        super().__init__()
    #
    # def optgroups(self, name, value, attrs=None):
    #     """Return a list of optgroups for this widget."""
    #     groups = []
    #     has_selected = False
    #
    #     for index, (option_value, option_label) in enumerate(self.choices):
    #         if option_value is None:
    #             option_value = ''
    #
    #         subgroup = []
    #         if isinstance(option_label, (list, tuple)):
    #             group_name = option_value
    #             subindex = 0
    #             choices = option_label
    #         else:
    #             group_name = None
    #             subindex = None
    #             choices = [(option_value, option_label)]
    #         groups.append((group_name, subgroup, index))
    #
    #         for subvalue, sublabel in choices:
    #             selected = (
    #                 str(subvalue) in value and
    #                 (not has_selected or self.allow_multiple_selected)
    #             )
    #             has_selected |= selected
    #             subgroup.append(self.create_option(
    #                 name, subvalue, sublabel, selected, index,
    #                 subindex=subindex, attrs=attrs,
    #             ))
    #             if subindex is not None:
    #                 subindex += 1
    #     return groups

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=None, attrs=None)
        if isinstance(value, int) and value % 2:
            option['attrs']['class'] = 'even'
        return option


class NestedSelectMultiple(widgets.SelectMultiple):
    def __init__(self):
        super().__init__()

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=None, attrs=None)
        if value % 2:
            option['attrs']['class'] = 'even'
        return option


# temp = widgets.Select

"""
value: 3, label: nazwa zespołu, level: 1, disabled: True
"""

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
        # self.fields['teams'] = NestedModelChoiceField(
        #     queryset=Team.objects.filter(
        #         category__organization__owner=self.request.user,
        #         # season_id=6,
        #         ).order_by('name')
        # )
        self.fields['teams'].widget = forms.SelectMultiple()
        temp = Team.get_choices(
            self.request.user,
            # organization_id=18,
            season_id=5,
            category_id=11,
        )
        self.fields['teams'].queryset = temp

        self.set_widget_attrs(FIELDS_ATTRS)

    class Meta:
        model = Game
        fields = ('id', 'category', 'season', 'teams', 'name', 'up_to_sets', 'scoring_system')
