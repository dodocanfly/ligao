from django import forms
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from apps.dashboard.models import Organization, Season, ClubCategory


class OrganizationCreateUpdateForm(forms.ModelForm):
    error_msg = {
        'object_not_exist': _('Obiekt, który chcesz edytować, nie istnieje na twoim koncie.'),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        object_exists = Organization.objects.filter(id=self.initial.get('id'), owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404(self.error_msg['object_not_exist'])

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['private'].widget.attrs['class'] = 'form-check-input'

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.owner = self.user
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        exclude = ['owner']


class SeasonAddEditForm(forms.ModelForm):
    error_msg = {
        'object_not_exist': _('Obiekt, który chcesz edytować, nie istnieje na twoim koncie.'),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        object_exists = Season.objects.filter(id=self.initial.get('id'), organization__owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404(self.error_msg['object_not_exist'])
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.user)
        self.fields['organization'].widget.attrs = {'class': 'form-control'}
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': _('np. sezon 2019/2020')}
        self.fields['start_year'].widget.attrs = {'class': 'form-control', 'placeholder': _('np. 2019')}
        self.fields['double_year'].widget.attrs = {'class': 'form-check-input'}

    class Meta:
        model = Season
        fields = '__all__'


class ClubCategoryAddEditForm(forms.ModelForm):
    error_msg = {
        'object_not_exist': _('Obiekt, który chcesz edytować, nie istnieje na twoim koncie.'),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        object_exists = ClubCategory.objects.filter(id=self.initial.get('id'), organization__owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404(self.error_msg['object_not_exist'])
        self.fields['organization'].queryset = Organization.objects.filter(owner=self.user)
        self.fields['organization'].widget.attrs = {'class': 'form-control'}
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': _('np. kluby młodzieżowe')}
        self.fields['parent'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = ClubCategory
        fields = '__all__'
