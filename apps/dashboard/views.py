from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from apps.dashboard.forms import OrganizationCreateUpdateForm
from apps.dashboard.models import Organization


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
    template_name = 'dashboard/organization_list.html'

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)


class OrganizationAddView(BaseCreateView):
    form_class = OrganizationCreateUpdateForm
    template_name = 'dashboard/organization_add.html'
    success_url = reverse_lazy('organization_list')


class OrganizationEditView(BaseUpdateView):
    model = Organization
    form_class = OrganizationCreateUpdateForm
    template_name = 'dashboard/organization_edit.html'
    success_url = reverse_lazy('organization_list')


class OrganizationDeleteView(BaseDeleteView):
    model = Organization
    template_name = 'dashboard/organization_delete.html'
    success_url = reverse_lazy('organization_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Organization.objects.filter(id=obj.id, owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj
