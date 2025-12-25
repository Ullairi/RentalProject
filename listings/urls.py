from django.urls import path
from . import views

urlpatterns = [
    path('listings/', views.ListingListView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('listings/create/', views.ListingCreateView.as_view(), name='listing-create'),
    path('listings/<int:pk>/manage/', views.ListingManageView.as_view(), name='listing-manage'),
    path('listings/<int:pk>/toggle-status/', views.toggle_listing_status, name='listing-toggle'),
    path('listings/<int:pk>/add-image/', views.add_listing_image, name='listing-add-image'),
    path('amenities/', views.AmenityListView.as_view(), name='amenity-list'),
]