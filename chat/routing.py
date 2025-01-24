from django.urls import path
from chat.consumers import ChatroomConsumer

chat_urlpatterns = [
    path("ws/chat/room/<uuid:chatname_room>/", ChatroomConsumer.as_asgi()),
]