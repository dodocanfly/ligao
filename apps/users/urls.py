from django.urls import path
from . import views

urlpatterns = [
    path('new', views.RegisterView.as_view(), name='register'),
    path('profil', views.ProfilView.as_view(), name='profil'),
]
