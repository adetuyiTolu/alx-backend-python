from django.shortcuts import render

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, CustomUserManager
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only conversations the current user is part of."""
        return Conversation.objects.filter(participants=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """Create a new conversation with given participants."""
        participants_ids = request.data.get('participants')
        if not participants_ids or not isinstance(participants_ids, list):
            return Response({"error": "Participants list is required."}, status=status.HTTP_400_BAD_REQUEST)

        participants = CustomUserManager.objects.filter(
            user_id__in=participants_ids)
        if not participants.exists():
            return Response({"error": "Invalid participant(s)."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        # Ensure the creator is part of the conversation
        conversation.participants.add(request.user)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['sent_at']
    search_fields = ['message_body']

    def get_queryset(self):
        """Return only messages from conversations the user is part of."""
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').order_by('sent_at')

    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation."""
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(
            Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
