from django.contrib import admin
from .models import Address, Amenity, Listing, ListingImg


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin configuration for address records"""
    list_display = ['street', 'city', 'postal_code', 'country']
    search_fields = ['city', 'street', 'postal_code']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Admin settings for amenities"""
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']

class ListingImageInline(admin.TabularInline):
    """Admin view for listing images"""
    model = ListingImg
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """Admin panel to configure listings"""
    list_display = ['title', 'owner', 'house_type', 'price_per_night', 'is_active', 'created_at']
    list_filter = ['house_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'address__city']
    inlines = [ListingImageInline]
    filter_horizontal = ['amenities']
