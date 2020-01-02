from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.restapi import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'game-categories', views.GameCategoryViewSet)
# router.register(r'seasons', views.SeasonViewSet)
# router.register(r'teams', views.TeamViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('gamedata/<int:id>', views.GameDataView.as_view())
]
