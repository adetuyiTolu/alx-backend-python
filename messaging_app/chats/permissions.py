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
