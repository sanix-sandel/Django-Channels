import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Obtain the room name from the url
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        #Constructs a Channels group name directly from the user-specified
        #room name
        self.room_group_name='chat_%s'%self.room_name
        
        #Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()#Accepts the Websocket connection
        #If you do not call accpet() method then the connection
        #will be rejected and closed


    async def disconnect(self, close_code):
        #Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    #Receive message from websocket
    async def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }#An event has a special 'type' key corresponding to
            #the name of the mrthod that should be invoked on 
            #consumers that receive the event
        )

    #Receive message from room group
    async def chat_message(self, event):
        message=event['message']

        #Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message':message
        }))    