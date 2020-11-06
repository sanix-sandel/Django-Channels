import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import*
from .serializers import*
from django.shortcuts import render, get_object_or_404

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        id=self.scope['user'].id
        print(self.scope)
        self.conversation_code=self.scope['url_route']['kwargs']['roomName']
        self.other_id=self.scope['url_route']['kwargs']['user2_id']
        self.other_id=int(self.other_id)

        self.thread=await self.get_thread_or_create_new_one()

        self.room_group_name=f'chat_{self.conversation_code}'
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()    


    async def receive(self, text_data):
        data=json.loads(text_data)
        msg_obj=await self.create_message(data)
        serializer=MessageSerializer(msg_obj, many=False)
        await self.channel_layer.group_send(self.room_group_name, 
                                            {'type':'chat_message',
                                            'message':msg_obj})

    async def chat_message(self, event):
        message=event['message']
        await self.send(text_data=json.dumps(
            {
                'message':message
            }
        ))                                        


    @database_sync_to_async
    def get_thread_or_create_new_one(self):
        try:
            thread=get_object_or_404(Conversation, code=self.conversation_code)
        except:
            user1=self.scope['user']
            user2=get_object_or_404(get_user_model(), id=self.other_id)
            users=[user1, user2]
            
            thread=Conversation.objects.create(code=str(user1.id)+str(user2))
            thread.users.set(users)
            thread.save()
            return thread
        return thread        


    @database_sync_to_async
    def create_message(self, data):
        serializer=MessageCreation(data=data)
        author_id=data['author_id']

        author=get_object_or_404(get_user_model(), id=author_id)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=author, conversation=self.thread)
            return serializer.data
        else:
            pass    


    async def disconnect(self, event):
        # Leave room group
        print(self.channel_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )