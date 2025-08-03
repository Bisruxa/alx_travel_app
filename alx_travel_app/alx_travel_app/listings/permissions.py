from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAnonymous(BasePermission):
    def has_permission(self, request, view): # type: ignore
        return request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True 
        return request.user.is_anonymous
    
class IsAdminOrUserOwner(BasePermission):
    def has_permission(self, request, view): # type: ignore
        return request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj