import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView )

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import User, Favorite
from .serializers import (UserSerializer, UserProfileSerializer,
    UserInfoUpdateSerializer, FavoriteSerializer )

from .services import UserService, FavoriteService

logger = logging.getLogger(__name__)


# User views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register new user
    POST /api/users/register/
    {
        "username": "test_joe",
        "email": "joe@test.com",
        "password": "TestTest123",
        "password_confirm": "TestTest123",
        "role": "tenant",
        "first_name": "Joe",
        "last_name": "Test"
    }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        validated_data.pop('password_confirmation')
        user = UserService.create_user(validated_data)

        return Response(
            UserProfileSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    Get list of all users
    GET /api/users/
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'gender']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']


class UserDetailView(RetrieveAPIView):
    """
    Get user by ID
    GET /api/users/{id}/
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current user profile
    GET /api/users/me/
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    UPdate current user profile
    PATCH /api/users/update-profile/
    """
    serializer = UserInfoUpdateSerializer(
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        updated_user = UserService.update_user_profile(
            request.user,
            serializer.validated_data
        )
        return Response(UserProfileSerializer(updated_user).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    """
    Get current user statistics
    GET /api/users/statistics/
    """
    stats = UserService.user_statistic(request.user)
    return Response(stats)


#Favouriye views
class FavoriteListCreateView(ListCreateAPIView):
    """
    Get user favorites / Add to favorites
    GET /api/favorites/
    POST /api/favorites/
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return only current user favorites"""
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('listing', 'user')

    def create(self, request, *args, **kwargs):
        """Add listing to favorites"""
        listing_id = request.data.get('listing_id')

        if not listing_id:
            return Response(
                {'error': 'listing_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            favorite = FavoriteService.add_listing_to_fav(
                request.user,
                listing_id
            )
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'Error adding to favorites: {str(e)}')
            return Response(
                {'error': 'Failed to add to favorites'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FavoriteDetailView(RetrieveUpdateDestroyAPIView):
    """
    Get / Delete favorite by ID
    GET /api/favorites/{id}/
    DELETE /api/favorites/{id}/
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        """Return only current user favorites"""
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('listing', 'user')

    def destroy(self, request, *args, **kwargs):
        """Remove from favorites"""
        favorite = self.get_object()
        favorite.delete()
        logger.info(
            f'User {request.user.email} removed from favorites: {favorite.listing_id}'
        )
        return Response(
            {'message': 'Removed from favorites'},
            status=status.HTTP_204_NO_CONTENT
        )