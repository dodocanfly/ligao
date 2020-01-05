from django.urls import path
from . import views

urlpatterns = [
    path('rozgrywki/lista', views.GameListView.as_view(), name='game-list'),
    path('rozgrywki/dodaj', views.GameAddView.as_view(), name='game-add'),
    path('rozgrywki/edytuj/<int:pk>', views.GameEditView.as_view(), name='game-edit'),
    path('rozgrywki/usun/<int:pk>', views.GameDeleteView.as_view(), name='game-delete'),
]
