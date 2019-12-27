from django.utils.translation import gettext_lazy as _


MAX_CAT_TREE_DEPTH = 5

FIELDS_ATTRS = {

    'OrganizationAddEditForm': {
        'name': {
            'class': 'form-control',
            'minlength': 3,
            'placeholder': _('np. MOSiR Ełk'),
        },
        'description': {
            'class': 'form-control',
            'rows': 5,
        },
        'location': {
            'class': 'form-control',
        },
        'private': {
            'class': 'form-check-input',
        },
    },

    'SeasonAddEditForm': {
        'organization': {
            'class': 'form-control'
        },
        'name': {
            'class': 'form-control',
            'minlength': 4,
            'placeholder': _('np. sezon 2019/2020'),
        },
        'start_year': {
            'class': 'form-control',
            'placeholder': _('np. 2019'),
        },
        'double_year': {
            'class': 'form-check-input',
        },
    },

    'ClubCategoryAddEditForm': {
        'name': {
            'class': 'form-control',
            'minlength': 5,
            'placeholder': _('np. kluby młodzieżowe'),
        },
        'organization': {
            'class': 'form-control',
        },
        'parent': {
            'class': 'form-control',
        },
    },

}
