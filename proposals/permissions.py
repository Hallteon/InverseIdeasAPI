from rest_framework import permissions


class IsProposalAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author.id == request.user.id
    
    
class IsInProposalHistories(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        for history in obj.histories:
            if request.user.id == history.by_user.id:
                return True