from django.utils.translation import gettext_lazy as _


FIELDS_ATTRS = {

    'Organization': {
        'name': {
            'class': 'form-control',
            'minlength': 3,
            'placeholder': 'np. MOSiR Ełk',
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

    'Season': {
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

    'ClubCategory': {
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
