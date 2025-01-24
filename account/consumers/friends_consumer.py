import json

from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from database.models import (
    User,
    Notification,
    Friendship
)

from account.serializers.friendship_serializer import FriendshipSerializer


class FriendsConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"user_friends_{self.user.username}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json["status"]
        
        recipient_id = text_data_json.get('recipient_user').get('id')
        recipient_username = text_data_json.get("recipient_user").get("username")
        
        sender_id = text_data_json.get('sender_user').get('id')
        sender_username = text_data_json.get("sender_user").get("username")
        
        print(recipient_id, recipient_username, sender_id, sender_username)
        
        recipient_user = self.get_user(recipient_id, recipient_username)
        sender_user = self.get_user(sender_id, sender_username)
        
        if not recipient_user or not sender_user:
            print("User not found")
            return
        
        self.handle_friendship_status(
            sender_user=sender_user, 
            recipient_user=recipient_user, 
            status=status
        )
        
    def get_user(self, user_id, username):
        if user_id:
            return User.objects.filter(id=user_id).first()
        if username:
            return User.objects.filter(username=username).first()

        return None
    
    def handle_friendship_status(self, sender_user, recipient_user, status):
        is_created_friendship = False
        
        if status == Friendship.Status.REQUESTED:
            friendship, is_created_friendship = Friendship.create_request(
                from_user=sender_user,
                to_user=recipient_user
            )
        elif status == Friendship.Status.ACCEPTED:
            friendship = self.accept_friendship(
                sender_user=sender_user,
                recipient_user=recipient_user
            )
        elif status == Friendship.Status.DECLINED:
            friendship = self.decline_friendship(
                sender_user=sender_user,
                recipient_user=recipient_user
            )
        elif status == Friendship.Status.BLOCKED:
            friendship = self.block_friendship(
                sender_user=sender_user,
                recipient_user=recipient_user
            )
        
        friendship_serializer = FriendshipSerializer(friendship)
        friendship_data = {
            **friendship_serializer.data,
            "is_created": is_created_friendship,   
        }
        
        event_friendship = {
            'type': "friendship_handler",
            'friendship': friendship_data,
        }   
        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            event_friendship
        )
        
    def accept_friendship(self, sender_user, recipient_user):
        friendship = Friendship.objects.get(
            from_user=sender_user,
            to_user=recipient_user
        )
        friendship.accept()
        self.delete_notification("send_friend", sender_user, recipient_user)
        return friendship
    
    def decline_friendship(self, sender_user, recipient_user):
        friendship = Friendship.objects.get(
            from_user=sender_user,
            to_user=recipient_user
        )
        friendship.decline()
        self.delete_notification("send_friend", sender_user, recipient_user)
        return friendship
    
    def block_friendship(self, sender_user, recipient_user):
        friendship = Friendship.objects.get(
            from_user=sender_user,
            to_user=recipient_user
        )
        friendship.blocked()
        self.delete_notification("send_friend", sender_user, recipient_user)
        return friendship
    
    def delete_notification(self, notification_type, sender_user, recipient_user):
        print(notification_type, sender_user, recipient_user)
        notification = Notification.objects.filter(
            type=notification_type,
            sender=sender_user,
            recipient=recipient_user
        ).first() #send_friend
        if not notification:
            print(f"No matching notification found for sender={sender_user.username}, recipient={recipient_user.username}")
            return {"notification_status": "not_found"}
    
        if notification.sender != sender_user or notification.recipient != recipient_user:
            print(f"Notification mismatch! Found sender={notification.sender.username}, recipient={notification.recipient.username}")
            return {"notification_status": "mismatch"}
        
        print(f"Notification sender: {notification.sender.username}, recipient: {notification.recipient.username}")

        print(notification)
        notification.delete()
        return {"notification_status": "deleted"}
    
    def friendship_handler(self, event):
        print('send friendship!!')
        friendship = event['friendship']
        self.send(text_data=json.dumps({
            "friendship": friendship,
            "status": {
                "send": "send_notifications",
                "type": "send_friend"
            }
        }))