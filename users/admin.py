from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Favorite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for user"""
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'role', 'is_active', 'created_at'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'gender']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        ('Account', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'gender', 'birth_date', 'phone')
        }),
        ('Role and status', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['last_login', 'created_at', 'updated_at']

    add_fieldsets = (
        ('User creation', {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'first_name', 'last_name', 'role'
            ),
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin interface for managing user wishlist"""
    list_display = ['user', 'listing', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__username', 'listing__title']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        """Request optimiyation"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'listing')
