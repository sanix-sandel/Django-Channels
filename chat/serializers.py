from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import*
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    author_id=serializers.UUIDField(source='author.id')
    conversation=serializers.CharField(source='conversation.code')
    class Meta:
        model=Message
        fields=('content', 'author_id', 'conversation', 'sent_on')

class MessageCreation(serializers.ModelSerializer):
    author_id=serializers.UUIDField(source='author.id')
    class Meta:
        model=Message
        fields=('content', 'author_id')


class ConversationSerializer(serializers.ModelSerializer):
    messages=serializers.SerializerMethodField('get_messages')
    class Meta:
        model=Conversation
        fields=('users', 'messages', 'code')

    def get_messages(self, conversation):
        messages=Message.objects.filter(conversation=conversation)
        serializer=MessageSerializer(messages, many=True)
        return serializer.data    