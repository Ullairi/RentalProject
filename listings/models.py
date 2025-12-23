from django.db import models
from core.mixins import TimestampMixin


class Listing(TimestampMixin):
    """Listing model for Favorite model from users/models relation"""
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'listings'

    def __str__(self):
        return self.title
