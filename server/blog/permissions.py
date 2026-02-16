from rest_framework.permissions import BasePermission

class BlogCreatePermissions(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_staff 
    
