import logging
from django.db import transaction
from .models import User, Favorite
from listings.models import Listing
from core.exceptions import AccessRightsError


logger = logging.getLogger(__name__)

class UserService:
    """Service for work with user"""
    @staticmethod
    def create_user(validated_data):
        """Creation of a new user"""
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            logger.info(f'Created new user: {user.email}')
            return user

    @staticmethod
    def update_user_profile(user, validated_data):
        """Update of user profile"""
        for field, val in validated_data.items():
            setattr(user, field, val)

        user.save()
        logger.info(f'User profile updated: {user.email}')
        return user

    @staticmethod
    def user_statistic(user):
        """Receive user statistic(e.g. amount of bookings, listings ...)"""
        stats = {
            'listing_count': 0,
            'bookings_count': 0,
            'reviews_count': 0,
            'favorites_count': user.favorites.count(),
        }

        if user.is_owner:
            stats['listing_count'] = user.listings.count()
            stats['bookings_received'] = sum(
                listing.bookings.count() for listing in user.listings.all()
            )

        if user.is_tenant:
            stats['bookings_count'] = user.bookings.count()
            stats['reviews_count'] = user.reviews.count()

        return stats

class FavoriteService:
    """Service to work with favorites(wishlist)"""
    @staticmethod
    def add_listing_to_fav(user, listing_id):
        try:
            listing = Listing.objects.get(id=listing_id, is_active=True)
        except Listing.DoesNotExist:
            raise ValueError('Listing was not found or is unavailable')

        if listing.owner == user:
            raise AccessRightsError(
                'You cant add your own listing to wishlist'
            )

        favorite, created = Favorite.objects.get_or_create(
            user=user,
            listing=listing
        )

        if not created:
            raise ValueError('Listing already wishlisted')

        logger.info(f'User {user.email} add in wishlist: {listing.title}')
        return favorite

    @staticmethod
    def remove_from_favorites(user, listing_id):
        """Removal of listing from wishlist"""
        try:
            favorite = Favorite.objects.get(user=user, listing_id=listing_id)
            favorite.delete()
            logger.info(f'User {user.email} removed listing from wishlist: {listing_id}')
            return True
        except Favorite.DoesNotExist:
            return False

    @staticmethod
    def user_favorited(user):
        """Receive all users wishlisted listings"""
        return Favorite.objects.filter(user=user).select_related('listing')