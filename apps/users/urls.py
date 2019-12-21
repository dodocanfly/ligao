from django.urls import path
from . import views

urlpatterns = [
    path('new', views.Register.as_view(), name='register'),
]
