
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWorker(BasePermission):
    """
    Custom permission to only allow workers to perform certain actions.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and their account_type is "Worker"
        return request.user.is_authenticated and request.user.account_type == "Worker"

class IsEmployer(BasePermission):
    """
    Custom permission to only allow employers to perform certain actions.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and their account_type is "Employer"
        return request.user.is_authenticated and request.user.account_type == "Employer"
    
    
class IsSenderOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read permissions to any request, but only allow writes if sender is requesting user
        return request.method in SAFE_METHODS or obj.sender == request.user
