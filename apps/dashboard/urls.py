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
    path('sezony/usun/<int:pk>', views.OrganizationDeleteView.as_view(), name='season-delete'),

    path('kluby/lista', views.SeasonListView.as_view(), name='club-list'),
    path('kluby/dodaj', views.SeasonAddView.as_view(), name='club-add'),
    path('kluby/edytuj/<int:pk>', views.SeasonEditView.as_view(), name='club-edit'),
    path('kluby/usun/<int:pk>', views.OrganizationDeleteView.as_view(), name='club-delete'),

    path('kategorie-klubow/lista', views.ClubCategoryListView.as_view(), name='club-category-list'),
    path('kategorie-klubow/dodaj', views.ClubCategoryAddView.as_view(), name='club-category-add'),
    path('kategorie-klubow/edytuj/<int:pk>', views.ClubCategoryEditView.as_view(), name='club-category-edit'),
    path('kategorie-klubow/usun/<int:pk>', views.ClubCategoryDeleteView.as_view(), name='club-category-delete'),
]
