from django.urls import path
from account.consumers.notification_consumer import NotificationConsumer
from account.consumers.friends_consumer import FriendsConsumer

account_urlpatterns = [
    path("ws/notification/", NotificationConsumer.as_asgi()),
    path("ws/create-friends/", FriendsConsumer.as_asgi()),
]