from rest_framework import permissions

class IsReviewAuthorOrReadOnly(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author or request.method in permissions.SAFE_METHODS) or super().has_permission(request, view) and request.method in ('GET', 'DELETE')

class IsOwnerOrReadOnly(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.owner or request.method in permissions.SAFE_METHODS) or super().has_permission(request, view) and request.method in ('GET', 'DELETE')
