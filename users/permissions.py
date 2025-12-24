from rest_framework import permissions


class AdminOrOwner(permissions.BasePermission):
    """
    Accessibility options only for admins and owners
    (e.g. profile/listings editing ...)
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return obj == request.user

class Admin(permissions.BasePermission):
    """
    Accessibility options only for admins
    (e.g. user management, sys. administration, moderation ...)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class Owner(permissions.BasePermission):
    """
    Accessibility options only for owners
    (e.g. creating/managing lists ...)
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_owner

class Tenant(permissions.BasePermission):
    """
    Accessibility options only for tenants
    (e.g. leaving reviews, book bookings ...)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tenant

class OwnerOrUserReadOnly(permissions.BasePermission):
    """
    Edit only for owner
    (list of amenities that only owner can modify,
    e.g. wi-fi, bathroom/kitchens type/amount mentioning)
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user

        return False