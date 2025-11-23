from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
            
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.sender == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj == request.user


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        elif hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        else:
            return obj == request.user


class CanCreateConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.role in ['host', 'admin', 'guest']
        return True


class CanSendMessage(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(
                user_id=request.user.user_id
            ).exists()
        return True