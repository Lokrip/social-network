import json

from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from database.models import (
    ChatGroup,
    GroupMessage
)

from django.utils.text import slugify


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatname_room = self.scope["url_route"]["kwargs"]["chatname_room"]
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatname_room)
        
        self.chatname_room_slugify = slugify(self.chatname_room)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatname_room_slugify,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatname_room_slugify,
            self.channel_name
        )
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json.get("body")
        
        message = GroupMessage.objects.create(
            body=body,
            user=self.user,
            group=self.chatroom
        )
        
        event = {
            "type": "message_handler",
            "body": message.body,
            "user": message.user.username
        }
        
        async_to_sync(self.channel_layer.group_send)(
            self.chatname_room_slugify,
            event
        )
        #создай чат для двух друзей при прнинятие в друзия 
    
    def message_handler(self, event):
        self.send(text_data=json.dumps({"body": event["body"], "user": event["user"]}))