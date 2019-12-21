from django import forms
from django.http import Http404

from apps.dashboard.models import Organization, Season, ClubCategory
from .forms_config import FIELDS_ATTRS


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def set_attrs_for(self, model_key):
        if model_key in FIELDS_ATTRS:
            for field, attrs in FIELDS_ATTRS[model_key].items():
                if field in self.fields:
                    self.fields[field].widget.attrs = attrs


class OrganizationCreateUpdateForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Organization.objects.filter(id=self.initial.get('id'), owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.set_attrs_for('Organization')

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.owner = self.user
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        exclude = ['owner']


class SeasonAddEditForm(MyModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = Season.objects.filter(id=self.initial.get('id'), organization__owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.user)
        self.set_attrs_for('Season')

    class Meta:
        model = Season
        fields = '__all__'


class ClubCategoryAddEditForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_exists = ClubCategory.objects.filter(id=self.initial.get('id'), organization__owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404('object not exist for user')
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.user)
        self.set_attrs_for('ClubCategory')

    class Meta:
        model = ClubCategory
        fields = '__all__'
