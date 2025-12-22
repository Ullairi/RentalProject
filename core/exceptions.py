from rest_framework.exceptions import APIException
from rest_framework import status


class ListingNotAvailableError(APIException):
    """Exception if listing is not available"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Listing is unavailable for booking'
    default_code = 'listing_not_available'

class BookingNotAvailableError(APIException):
    """Exception if there is a booking conflict(e.g. date overlapping)"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Chosen dates are unavailable for booking'
    default_code = 'booking_not_available'