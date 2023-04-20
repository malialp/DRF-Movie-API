from rest_framework import permissions


class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author.user or request.method in permissions.SAFE_METHODS or request.user.is_staff and request.method in ('GET', 'DELETE')


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner.user or request.method in permissions.SAFE_METHODS or request.user.is_staff and request.method in ('GET', 'DELETE')
    

class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user or request.method in permissions.SAFE_METHODS) and request.method != 'DELETE'
