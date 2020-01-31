from django import forms
from django.utils.safestring import mark_safe


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

    def set_widget_attrs(self, source=None):
        if source is None:
            return None
        model_key = self.__class__.__name__
        if model_key in source:
            for field, attrs in source[model_key].items():
                if field in self.fields:
                    self.fields[field].widget.attrs = attrs
