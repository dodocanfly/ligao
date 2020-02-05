from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from django.utils.translation import ugettext_lazy as _

from apps.dashboard.forms import (
    OrganizationAddEditForm,
    SeasonAddEditForm,
    ClubCategoryAddEditForm,
    ClubAddEditForm,
    TeamCategoryAddEditForm,
    TeamAddEditForm,
    GameCategoryAddEditForm,
    GameAddForm)
from apps.dashboard.models import (
    Organization,
    Season,
    ClubCategory,
    Club,
    TeamCategory,
    Team,
    GameCategory,
)


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


"""
##############################################################################
                             BASE GENERIC VIEWS
##############################################################################
"""


class BaseListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 25


class BaseCreateView(LoginRequiredMixin, generic.CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def set_success_urls(self):
        return ['url-to-list', 'url-to-add-form']  # or string instead list for the same url

    def get_success_url(self):
        urls = self.set_success_urls()
        list_url = urls[0] if isinstance(urls, list) else str(urls)
        form_url = urls[1] if isinstance(urls, list) and len(urls) > 1 else list_url
        if self.request.POST.get('another-one'):
            return reverse_lazy(form_url)
        else:
            return reverse_lazy(list_url) + '?ok=1'


class BaseUpdateView(LoginRequiredMixin, generic.UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def set_success_urls(self):
        return ['url-to-list', 'url-to-add-form']  # or string instead list for the same url

    def get_success_url(self):
        urls = self.set_success_urls()
        list_url = urls[0] if isinstance(urls, list) else str(urls)
        form_url = urls[1] if isinstance(urls, list) and len(urls) > 1 else list_url
        if self.request.POST.get('another-one'):
            return reverse_lazy(form_url)
        else:
            return reverse_lazy(list_url) + '?ok=1'


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    permission_error = 'Nie masz uprawnień do usunięcia tego obiektu.'

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            context = self.get_context_data()
            context.update({'cant_delete': True})
            return render(request, template_name=self.template_name, context=context)


"""
##############################################################################
                             ORGANIZATIONS VIEWS
##############################################################################
"""


class OrganizationListView(BaseListView):
    template_name = 'dashboard/organization-list.html'

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)


class OrganizationAddView(BaseCreateView):
    form_class = OrganizationAddEditForm
    template_name = 'dashboard/organization-add.html'

    def set_success_urls(self):
        return ['organization-list', 'organization-add']


class OrganizationEditView(BaseUpdateView):
    model = Organization
    form_class = OrganizationAddEditForm
    template_name = 'dashboard/organization-edit.html'

    def set_success_urls(self):
        return ['organization-list', 'organization-add']


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
##############################################################################
                               SEASONS VIEWS
##############################################################################
"""


class SeasonListView(BaseListView):
    template_name = 'dashboard/season-list.html'

    def get_queryset(self):
        return Organization.all_with_seasons(self.request.user)
        # return Season.objects.filter(organization__owner=self.request.user)


class SeasonAddView(BaseCreateView):
    form_class = SeasonAddEditForm
    template_name = 'dashboard/season-add.html'

    def set_success_urls(self):
        return ['season-list', 'season-add']


class SeasonEditView(BaseUpdateView):
    model = Season
    form_class = SeasonAddEditForm
    template_name = 'dashboard/season-edit.html'

    def set_success_urls(self):
        return ['season-list', 'season-add']


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
##############################################################################
                            CLUB CATEGORIES VIEWS
##############################################################################
"""


class ClubCategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/club_category-list.html'
        try:
            if request.GET.get('c'):
                template_name = 'dashboard/club_category-list-eq.html'
                object_list = ClubCategory.get_one(request.user, request.GET.get('c'))
            elif request.GET.get('o'):
                object_list = Organization.get_one_with_club_categories(request.user, request.GET.get('o'))
            else:
                object_list = Organization.get_all_with_club_categories(request.user)
        except ValueError:
            raise Http404()
        return render(request, template_name, {
            'object_list': object_list,
        })


class ClubCategoryAddView(BaseCreateView):
    form_class = ClubCategoryAddEditForm
    template_name = 'dashboard/club_category-add.html'

    def set_success_urls(self):
        return ['club-category-list', 'club-category-add']


class ClubCategoryEditView(BaseUpdateView):
    model = ClubCategory
    form_class = ClubCategoryAddEditForm
    template_name = 'dashboard/club_category-edit.html'

    def set_success_urls(self):
        return ['club-category-list', 'club-category-add']


class ClubCategoryDeleteView(BaseDeleteView):
    model = ClubCategory
    template_name = 'dashboard/club_category-delete.html'
    success_url = reverse_lazy('club-category-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not ClubCategory.objects.filter(id=obj.id, organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
##############################################################################
                                 CLUBS VIEWS
##############################################################################
"""


class ClubListView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/club-list.html'
        try:
            if request.GET.get('c'):
                template_name = 'dashboard/club-list-eq.html'
                object_list = ClubCategory.get_one(request.user, request.GET.get('c'))
            elif request.GET.get('o'):
                object_list = Organization.get_one_with_clubs(request.user, request.GET.get('o'))
            else:
                object_list = Organization.get_all_with_clubs(request.user)
        except ValueError:
            raise Http404()
        return render(request, template_name, {
            'object_list': object_list,
        })


class ClubAddView(BaseCreateView):
    form_class = ClubAddEditForm
    template_name = 'dashboard/club-add-edit.html'
    extra_context = {'page_title': _('Dodaj nowy klub')}

    def set_success_urls(self):
        return ['club-list', 'club-add']


class ClubEditView(BaseUpdateView):
    model = Club
    form_class = ClubAddEditForm
    template_name = 'dashboard/club-add-edit.html'
    extra_context = {'page_title': _('Edytuj klub')}

    def set_success_urls(self):
        return ['club-list', 'club-add']


class ClubDeleteView(BaseDeleteView):
    model = Club
    template_name = 'dashboard/club-delete.html'
    success_url = reverse_lazy('club-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Club.objects.filter(id=obj.id, category__organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
##############################################################################
                            TEAM CATEGORIES VIEWS
##############################################################################
"""


class TeamCategoryListView(BaseListView):
    template_name = 'dashboard/team_category-list.html'

    def get_queryset(self):
        return Organization.get_all_with_team_categories(self.request.user)


class TeamCategoryAddView(BaseCreateView):
    form_class = TeamCategoryAddEditForm
    template_name = 'dashboard/team_category-add.html'

    def set_success_urls(self):
        return ['team-category-list', 'team-category-add']


class TeamCategoryEditView(BaseUpdateView):
    model = TeamCategory
    form_class = TeamCategoryAddEditForm
    template_name = 'dashboard/team_category-edit.html'

    def set_success_urls(self):
        return ['team-category-list', 'team-category-add']


class TeamCategoryDeleteView(BaseDeleteView):
    model = TeamCategory
    template_name = 'dashboard/team_category-delete.html'
    success_url = reverse_lazy('team-category-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not TeamCategory.objects.filter(id=obj.id, organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
##############################################################################
                                 TEAMS VIEWS
##############################################################################
"""


class TeamListView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/team-list.html'
        try:
            if request.GET.get('c'):
                template_name = 'dashboard/team-list-eq.html'
                object_list = TeamCategory.get_one(request.user, request.GET.get('c'))
            elif request.GET.get('o'):
                object_list = Organization.get_one_with_teams(request.user, request.GET.get('o'))
            elif request.GET.get('s'):
                object_list = Organization.get_one_with_teams(request.user, request.GET.get('o'))
            else:
                object_list = Organization.get_all_with_teams(request.user)
        except ValueError:
            raise Http404()
        return render(request, template_name, {
            'object_list': object_list,
        })


class TeamListViewGV(BaseListView):
    template_name = 'dashboard/team-list.html'

    def get_queryset(self):
        return Organization.get_all_with_teams(self.request.user)


class TeamAddView(BaseCreateView):
    form_class = TeamAddEditForm
    template_name = 'dashboard/team-add.html'

    def set_success_urls(self):
        return ['team-list', 'team-add']


class TeamEditView(BaseUpdateView):
    model = Team
    form_class = TeamAddEditForm
    template_name = 'dashboard/team-edit.html'

    def set_success_urls(self):
        return ['team-list', 'team-add']


class TeamDeleteView(BaseDeleteView):
    model = Team
    template_name = 'dashboard/team-delete.html'
    success_url = reverse_lazy('team-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not Team.objects.filter(id=obj.id, category__organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
##############################################################################
                            GAME CATEGORIES VIEWS
##############################################################################
"""


class GameCategoryListView(BaseListView):
    template_name = 'dashboard/game_category-list.html'

    def get_queryset(self):
        return Organization.get_all_with_game_categories(self.request.user)


class GameCategoryAddView(BaseCreateView):
    form_class = GameCategoryAddEditForm
    template_name = 'dashboard/game_category-add.html'

    def set_success_urls(self):
        return ['game-category-list', 'game-category-add']


class GameCategoryEditView(BaseUpdateView):
    model = GameCategory
    form_class = GameCategoryAddEditForm
    template_name = 'dashboard/game_category-edit.html'

    def set_success_urls(self):
        return ['game-category-list', 'game-category-add']


class GameCategoryDeleteView(BaseDeleteView):
    model = GameCategory
    template_name = 'dashboard/game_category-delete.html'
    success_url = reverse_lazy('game-category-list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not GameCategory.objects.filter(id=obj.id, organization__owner=self.request.user).exists():
            raise PermissionError(self.permission_error)
        return obj


"""
##############################################################################
                            GAME CATEGORIES VIEWS
##############################################################################
"""


class GameListView(BaseListView):
    template_name = 'dashboard/game-list.html'

    def get_queryset(self):
        return Organization.get_all_with_game_categories(self.request.user)


class GameAddView(View):
    def get(self, request):
        form = GameAddForm(request=request)
        return render(request, 'dashboard/game-add.html', {'form': form})
