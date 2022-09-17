from rest_framework import permissions


class OnlyAdminCreate(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user.is_superuser:
            return False
        return super().has_permission(request, view)
