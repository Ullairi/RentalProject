import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer, BookingDetailSerializer, BookingCreateSerializer
from .services import BookingService
from users.permissions import Tenant

logger = logging.getLogger(__name__)


class BookingListCreateView(ListCreateAPIView):
    """
    Create new booking and list all tenants bookings
    GET /api/bookings/
    POST /api/bookings/
    """
    permission_classes = [Tenant]

    def get_serializer_class(self):
        """Return serializer depenging on request method"""
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Return bookings that belong to tenant"""
        return Booking.objects.filter(
            tenant=self.request.user
        ).select_related('listing', 'tenant')

    def perform_create(self, serializer):
        """Create booking using booking services"""
        booking = BookingService.create_booking(
            self.request.user,
            serializer.validated_data
        )
        serializer.instance = booking

class BookingDetailView(RetrieveAPIView):
    """
    Retrieves detailed info about booking
    GET /api/bookings/{id}/
    """
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        """Return bookings that user can access"""
        user = self.request.user
        if user.is_admin:
            return Booking.objects.all()

        return Booking.objects.filter(
            tenant=user
        ) | Booking.objects.filter(
            listing__owner=user
        )

class OwnerBookingsView(ListAPIView):
    """
    List bookings related to listings that owned by user
    GET /api/bookings/received/
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return bookings for listings that owned by user"""
        return Booking.objects.filter(
            listing__owner=self.request.user
        ).select_related('tenant', 'listing')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_booking(request, pk):
    """
    Confirm booking by listing owner
    POST /api/bookings/{id}/confirm/
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        booking = BookingService.confirm_booking(booking, request.user)
        return Response({
            'id': booking.id,
            'book_status': booking.book_status,
            'message': 'Booking confirmed'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_booking(request, pk):
    """
    Reject booking by listing owner
    POST /api/bookings/{id}/reject/
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        reason = request.data.get('reason', '')
        booking = BookingService.reject_booking(booking, request.user, reason)
        return Response({
            'id': booking.id,
            'book_status': booking.book_status,
            'message': 'Booking rejected'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, pk):
    """
    Cancel booking by tenant
    POST /api/bookings/{id}/cancel/
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        booking = BookingService.cancel_booking(booking, request.user)
        return Response({
            'id': booking.id,
            'book_status': booking.book_status,
            'message': 'Booking cancelled'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

