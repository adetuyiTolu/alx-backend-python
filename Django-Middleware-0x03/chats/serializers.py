# messaging_app/serializers/user_serializer.py

from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def get_sender(self, obj):
        return obj.sender.email


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(
        many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants.")
        return value
