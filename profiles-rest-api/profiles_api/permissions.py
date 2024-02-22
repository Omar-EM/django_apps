from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow a user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile
            Gets called, when we try to update new profile
        """

        # Check if save HTTP Method (like GET):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

