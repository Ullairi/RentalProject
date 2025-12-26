from django.db import models
from django.utils import timezone
from core.validators import validate_future_date
from core.mixins import TimestampMixin
from core.enums import BookingStatus
from django.core.exceptions import ValidationError


class Booking(TimestampMixin):
    """Class that represents booking made by a user for specific listing"""
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    stayers = models.PositiveIntegerField()
    check_in = models.DateField(validators=[validate_future_date])
    check_out =  models.DateField(validators=[validate_future_date])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    book_status = models.CharField(max_length=20, choices=BookingStatus.choices(),
                                   default=BookingStatus.pending.name)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['tenant']),
            models.Index(fields=['check_in']),
            models.Index(fields=['book_status']),
        ]

    def __str__(self):
        return f'Booking {self.id} - {self.listing.title} ({self.book_status})'

    def clean(self):
        """Simple validation for number of stayers and booking dates"""
        if self.check_out <= self.check_in:
            raise ValidationError('Check-in cant be before Check-out date')
        if self.stayers > self.listing.max_stayers:
            raise ValidationError(f'Only {self.listing.max_stayers} stayers allowed')

    @property
    def nights_to_stay(self):
        """Return certain number of nights between check-in and check-out"""
        return (self.check_out - self.check_in).days

    @property
    def cancelation(self):
        """Shows if the booking still can be canceled"""
        return (
            self.book_status in [BookingStatus.pending.name, BookingStatus.confirmed.name]
            and
            self.check_in > timezone.now().date()
        )

class BookingStatusHistory(TimestampMixin):
    """Class that stores all booking status changes of a specific listings"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_history')
    history_status = models.CharField(max_length=20, choices=BookingStatus.choices())
    comment = models.TextField(blank=True)
    changed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'booking_status_history'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking.id} - {self.history_status}'
