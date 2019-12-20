from django import forms
from django.http import Http404

from apps.dashboard.models import Organization


class OrganizationCreateUpdateForm(forms.ModelForm):
    error_msg = {
        'object_not_exist': 'Obiekt, który chcesz edytować, nie istnieje na twoim koncie.',
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        object_exists = Organization.objects.filter(id=self.initial.get('id'), owner=self.user).exists()
        if self.initial and not object_exists:
            raise Http404(self.error_msg['object_not_exist'])

    def save(self, commit=True):
        organization = super().save(commit=False)
        organization.owner = self.user
        if commit:
            organization.save()
        return organization

    class Meta:
        model = Organization
        exclude = ['owner']
