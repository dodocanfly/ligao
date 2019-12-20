from django.urls import path
from . import views

urlpatterns = [
    path('organizacje/lista', views.OrganizationListView.as_view(), name='organization_list'),
    path('organizacje/dodaj', views.OrganizationAddView.as_view(), name='organization_add'),
    path('organizacje/edytuj/<int:pk>', views.OrganizationEditView.as_view(), name='organization_edit'),
    path('organizacje/usun/<int:pk>', views.OrganizationDeleteView.as_view(), name='organization_delete'),
]
