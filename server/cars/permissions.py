from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsAuthorImage(BasePermission):
    
     def has_object_permission(self, request, view, obj):
         return obj.car.author == request.user