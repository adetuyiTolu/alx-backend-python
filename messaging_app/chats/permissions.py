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
    Allow only authenticated users who are participants in the conversation
    to view, update, or delete messages/conversations.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated for all API access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods like GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return self._is_participant(request, obj)

        # Allow PATCH, PUT, DELETE only if the user is a participant
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return self._is_participant(request, obj)

        # POST permissions can be handled in view or serializers if needed
        return self._is_participant(request, obj)

    def _is_participant(self, request, obj):
        # For Conversation objects directly
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For related objects like Message which has a conversation
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()

        return False
