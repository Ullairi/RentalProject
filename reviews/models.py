from django.db import models
from core.mixins import TimestampMixin
from core.validators import validate_rating


class Review(TimestampMixin):
    """Review model for listings"""
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(validators=[validate_rating])
    comment = models.TextField()

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ('listing', 'author')

    def __str__(self):
        return f'Review by {self.author.username} for {self.listing.title}'
