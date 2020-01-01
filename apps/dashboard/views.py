from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from apps.dashboard.forms import OrganizationAddEditForm, SeasonAddEditForm, ClubCategoryAddEditForm, ClubAddEditForm
from apps.dashboard.models import Organization, Season, ClubCategory, Club


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


"""
            BASE GENERIC VIEWS
"""


class BaseListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 25


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BaseUpdateView(LoginRequiredMixin, generic.UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    permission_error = 'Nie masz uprawnień do usunięcia tego obiektu.'
    protected_error = 'Obiekt powiązany jest z innymi obiektami i nie może być usunięty. <a href="javascript:history.back()">wwwwrrróć!!</a>'

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            return HttpResponseForbidden(self.protected_error)


"""
            ORGANIZATIONS VIEWS
"""


class OrganizationListView(BaseListView):
    template_name = 'dashboard/organization-list.html'

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)


class OrganizationAddView(BaseCreateView):
    form_class = OrganizationAddEditForm
    template_name = 'dashboard/organization-add.html'
    success_url = reverse_lazy('organization-list')


class OrganizationEditView(BaseUpdateView):
    model = Organization
    form_class = OrganizationAddEditForm
    template_name = 'dashboard/organization-edit.html'
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(BaseDeleteView):
    model = Organization
    template_name = 'dashboard/organization-delete.html'
    success_url = reverse_lazy('organization-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Organization.objects.filter(id=obj.id, owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
            SEASONS VIEWS
"""


class SeasonListView(BaseListView):
    template_name = 'dashboard/season-list.html'

    def get_queryset(self):
        return Season.objects.filter(organization__owner=self.request.user)


class SeasonAddView(BaseCreateView):
    form_class = SeasonAddEditForm
    template_name = 'dashboard/season-add.html'
    success_url = reverse_lazy('season-list')


class SeasonEditView(BaseUpdateView):
    model = Season
    form_class = SeasonAddEditForm
    template_name = 'dashboard/season-edit.html'
    success_url = reverse_lazy('season-list')


class SeasonDeleteView(BaseDeleteView):
    model = Season
    template_name = 'dashboard/season-delete.html'
    success_url = reverse_lazy('season-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Season.objects.filter(id=obj.id, organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
            CLUB CATEGORIES VIEWS
"""


class ClubCategoryListView(BaseListView):
    template_name = 'dashboard/club-category-list.html'

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)
        # return ClubCategory.objects.filter(organization__owner=self.request.user)


class ClubCategoryAddView(BaseCreateView):
    form_class = ClubCategoryAddEditForm
    template_name = 'dashboard/club-category-add.html'
    success_url = reverse_lazy('club-category-list')


class ClubCategoryEditView(BaseUpdateView):
    model = ClubCategory
    form_class = ClubCategoryAddEditForm
    template_name = 'dashboard/club-category-edit.html'
    success_url = reverse_lazy('club-category-list')


class ClubCategoryDeleteView(BaseDeleteView):
    model = ClubCategory
    template_name = 'dashboard/club-category-delete.html'
    success_url = reverse_lazy('club-category-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not ClubCategory.objects.filter(id=obj.id, organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
            CLUBS VIEWS
"""


class ClubListView(BaseListView):
    template_name = 'dashboard/club-list.html'

    def get_queryset(self):
        return Club.objects.filter(category__organization__owner=self.request.user)


class ClubAddView(BaseCreateView):
    form_class = ClubAddEditForm
    template_name = 'dashboard/club-add.html'
    success_url = reverse_lazy('club-list')


class ClubEditView(BaseUpdateView):
    model = Club
    form_class = ClubAddEditForm
    template_name = 'dashboard/club-edit.html'
    success_url = reverse_lazy('club-list')


class ClubDeleteView(BaseDeleteView):
    model = Club
    template_name = 'dashboard/club-delete.html'
    success_url = reverse_lazy('club-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Club.objects.filter(id=obj.id, category__organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj
