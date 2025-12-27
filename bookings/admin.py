from django.contrib import admin
from .models import Booking, BookingStatusHistory


class BookingStatusHistoryInline(admin.TabularInline):
    """Shows inline booking status history"""
    model = BookingStatusHistory
    extra = 0
    readonly_fields = ['history_status', 'comment', 'changed_by', 'created_at']
    can_delete = False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for bookings"""
    list_display = [
        'id', 'tenant', 'listing', 'check_in', 'check_out',
        'book_status', 'total_price', 'created_at'
    ]
    list_filter = ['book_status', 'check_in', 'created_at']
    search_fields = ['tenant__username', 'listing__title']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [BookingStatusHistoryInline]

    def get_queryset(self, request):
        """Optimized queries with related objects"""
        return super().get_queryset(request).select_related('tenant', 'listing')

@admin.register(BookingStatusHistory)
class BookingStatusHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for booking status history"""
    list_display = ['id', 'booking', 'history_status', 'changed_by', 'created_at']
    list_filter = ['history_status', 'created_at']
    readonly_fields = ['booking', 'history_status', 'comment', 'changed_by', 'created_at']

    def has_add_permission(self, request):
        """Prevent from manual creation of history records"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of history records"""
        return False