from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from .forms_config import MAX_CAT_TREE_DEPTH


def valid_max_tree_depth(current_category):
    def inner_validator(parent):
        if current_category.id is None:
            distance_to_farthest_leaf = 0
        else:
            distance_to_farthest_leaf = current_category.distance_to_farthest_leaf()
        total_depth = parent.distance_to_root() + distance_to_farthest_leaf + 2
        if total_depth > MAX_CAT_TREE_DEPTH:
            raise ValidationError(
                _('Przekroczona maksymalna głębokość drzewa kategorii (maksymalna: %(max)s, aktualna: %(total)s)') %
                {'max': MAX_CAT_TREE_DEPTH, 'total': total_depth}
            )
    return inner_validator


def valid_am_i_in_myself(current_category):
    def inner_validator(parent):
        if current_category.id is not None and parent.am_i_in_myself(current_category):
            raise ValidationError(_('Kategoria nadrzędna nie może leżeć poniżej kategorii edytowanej'))
    return inner_validator


def valid_same_organization(form):
    def inner_validator(parent):
        curr_cat_organization = form.cleaned_data.get('organization')
        if curr_cat_organization is not None and parent.organization_id != curr_cat_organization.id:
            raise ValidationError(_('Kategorie obecna i nadrzędna należą do różnych organizacji'))
    return inner_validator


def valid_can_change_org(instance):
    def inner_validator(organization):
        if instance.id is not None and instance.get_children() and instance.organization_id != organization.id:
            raise ValidationError(_('Nie można zmienić organizacji kategorii posiadającej podkategorię'))
    return inner_validator
