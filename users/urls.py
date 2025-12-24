from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='user-register'),

    # Users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/me/', views.current_user, name='user-me'),
    path('users/update-profile/', views.update_profile, name='user-update-profile'),
    path('users/statistics/', views.user_statistics, name='user-statistics'),

    # Favorites
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:pk>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),
    ]