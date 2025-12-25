from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Listing, Amenity
from .serializers import (
    ListingSerializer, ListingDetailSerializer,
    ListingCreateSerializer, AmenitySerializer,
    ListingImgSerializer
)
from .services import ListingService
from users.permissions import Owner, AdminOrOwner


class ListingListView(ListAPIView):
    """
    Return list of currentle active listings
    GET /api/listings/
    """
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get listings with advanced filters"""
        return ListingService.search_listings(self.request.query_params)

class ListingDetailView(RetrieveAPIView):
    """
    Return detailed info about 1 listing
    GET /api/listings/{id}/
    """
    queryset = Listing.objects.filter(is_active=True).select_related(
        'owner', 'address'
    ).prefetch_related('amenities', 'images')
    serializer_class = ListingDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        """Retrieve listing and increment views"""
        instance = self.get_object()
        ListingService.increment_views(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ListingCreateView(ListCreateAPIView):
    """
    Creating of a new listing
    POST /api/listings/create/
    """
    serializer_class = ListingCreateSerializer
    permission_classes = [Owner]

    def get_queryset(self):
        """Get current user listings"""
        return Listing.objects.filter(owner=self.request.user)

class ListingManageView(RetrieveUpdateDestroyAPIView):
    """
    Provide full access to a listing management(only for admin/owner)
    GET /api/listings/{id}/manage/
    PUT /api/listings/{id}/manage/
    DELETE /api/listings/{id}/manage/
    """
    serializer_class = ListingCreateSerializer
    permission_classes = [AdminOrOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        """Get listings user can manage"""
        if self.request.user.is_admin:
            return Listing.objects.all()
        return Listing.objects.filter(owner=self.request.user)

@api_view(['POST'])
@permission_classes([AdminOrOwner])
def toggle_listing_status(request, pk):
    """
    Allow switching between active and inactive status
    POST /api/listings/{id}/toggle-status/
    """
    try:
        if request.user.is_admin:
            listing = Listing.objects.get(pk=pk)
        else:
            listing = Listing.objects.get(pk=pk, owner=request.user)
    except Listing.DoesNotExist:
        return Response(
            {'error': 'Listing not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    listing = ListingService.toggle_active_status(listing)
    return Response({
        'id': listing.id,
        'is_active': listing.is_active,
        'message': f'Listing {"activated" if listing.is_active else "deactivated"}'
    })

class AmenityListView(ListAPIView):
    """
    Return all available amenities
    GET /api/amenities/
    """
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([Owner])
def add_listing_image(request, pk):
    """
    Adding image for a listing
    POST /api/listings/{id}/add-image/
    """
    try:
        listing = Listing.objects.get(pk=pk, owner=request.user)
    except Listing.DoesNotExist:
        return Response(
            {'error': 'Listing not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    img = request.FILES.get('image')
    if not img:
        return Response(
            {'error': 'Image file is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    main = request.data.get('main', 'false').lower() == 'true'
    img_obj = ListingService.add_image(listing, img, main)

    serializer = ListingImgSerializer(img_obj, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)
