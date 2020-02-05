from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.restapi import views

app_name = 'restapi'

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'game-categories', views.GameCategoryViewSet)
router.register(r'club-categories', views.ClubCategoryViewSet, basename='api-club-categories')
router.register(r'team-categories', views.TeamCategoryViewSet, basename='api-team-categories')
router.register(r'clubs', views.ClubViewSet, basename='api-clubs')
router.register(r'seasons', views.SeasonViewSet, basename='api-seasons')
router.register(r'teams', views.TeamViewSet, basename='api-teams')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('gamedata/<int:id>', views.GameDataView.as_view())
]
