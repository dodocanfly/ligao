from django.utils.translation import gettext_lazy as _


FIELDS_ATTRS = {

    'GameAddEditForm': {
        'category': {
            'class': 'form-control',
        },
        'season': {
            'class': 'form-control',
        },
        'teams': {
            'class': 'form-control',
            'size': 10,
        },
        'name': {
            'class': 'form-control',
            'minlength': 5,
            'placeholder': _('np. runda zasadnicza'),
        },
        'up_to_sets': {
            'class': 'form-control',
        },
        'scoring_system': {
            'class': 'form-control',
        },
    },

}
