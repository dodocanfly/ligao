from django.urls import path
from . import views

urlpatterns = [
    path('organizacje/lista', views.OrganizationListView.as_view(), name='organization-list'),
    path('organizacje/dodaj', views.OrganizationAddView.as_view(), name='organization-add'),
    path('organizacje/edytuj/<int:pk>', views.OrganizationEditView.as_view(), name='organization-edit'),
    path('organizacje/usun/<int:pk>', views.OrganizationDeleteView.as_view(), name='organization-delete'),

    path('sezony/lista', views.SeasonListView.as_view(), name='season-list'),
    path('sezony/dodaj', views.SeasonAddView.as_view(), name='season-add'),
    path('sezony/edytuj/<int:pk>', views.SeasonEditView.as_view(), name='season-edit'),
    path('sezony/usun/<int:pk>', views.SeasonDeleteView.as_view(), name='season-delete'),

    path('kluby/lista', views.ClubListView.as_view(), name='club-list'),
    path('kluby/dodaj', views.ClubAddView.as_view(), name='club-add'),
    path('kluby/edytuj/<int:pk>', views.ClubEditView.as_view(), name='club-edit'),
    path('kluby/usun/<int:pk>', views.ClubDeleteView.as_view(), name='club-delete'),

    path('kategorie-klubow/lista', views.ClubCategoryListView.as_view(), name='club-category-list'),
    path('kategorie-klubow/dodaj', views.ClubCategoryAddView.as_view(), name='club-category-add'),
    path('kategorie-klubow/edytuj/<int:pk>', views.ClubCategoryEditView.as_view(), name='club-category-edit'),
    path('kategorie-klubow/usun/<int:pk>', views.ClubCategoryDeleteView.as_view(), name='club-category-delete'),

    path('zespoly/lista', views.TeamListView.as_view(), name='team-list'),
    path('zespoly/dodaj', views.TeamAddView.as_view(), name='team-add'),
    path('zespoly/edytuj/<int:pk>', views.TeamEditView.as_view(), name='team-edit'),
    path('zespoly/usun/<int:pk>', views.TeamDeleteView.as_view(), name='team-delete'),

    path('kategorie-zespolow/lista', views.TeamCategoryListView.as_view(), name='team-category-list'),
    path('kategorie-zespolow/dodaj', views.TeamCategoryAddView.as_view(), name='team-category-add'),
    path('kategorie-zespolow/edytuj/<int:pk>', views.TeamCategoryEditView.as_view(), name='team-category-edit'),
    path('kategorie-zespolow/usun/<int:pk>', views.TeamCategoryDeleteView.as_view(), name='team-category-delete'),
]
