import json

from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from database.models import (
    User,
    Notification,
    Friendship
)

from account.serializers.notification_serializer import NotificationSerializer

class StatusSending:
    SEND_NOTIFICATIONS = "send_notifications"

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"user_notification_{self.user.username}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        data = text_data_json["data"]
        recipient_username = text_data_json.get("recipient_username")
        
        status_send = text_data_json["send"]
        type_send = text_data_json["type_send"]
        
        recipient_user = User.objects.get(username=recipient_username)

        notification, is_created_notification = Notification.objects.get_or_create(
            sender=self.user,
            recipient=recipient_user,
            type=type_send,
            defaults={"content": ""}
        )
    
        notification_serializer = NotificationSerializer(notification)
        notification_data = {
            **notification_serializer.data,
            "is_created": is_created_notification, 
        }
        
        #ошибка в том что когда мы отпровляем уведомлние пользователя так как он не был при коннектен к группе то мы отпровляем не извесному человеку и происходит ошибка
        notification_event = {
            'type': "notification_handler",
            "notification": notification_data
        }
        recipient_user_group_name = f"user_notification_{recipient_user.username}"
        
        async_to_sync(self.channel_layer.group_send)(
            recipient_user_group_name,
            notification_event
        )
        
    def notification_handler(self, event):
        notification = event["notification"]
        response = {"data": notification, "status": "success"}
        self.send(text_data=json.dumps(response))
        