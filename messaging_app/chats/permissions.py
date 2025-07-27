from .models import Conversation
from rest_framework import permissions


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow users to view their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Check that user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check that the user is a participant in the conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
