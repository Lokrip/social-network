from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("list/", views.ChatListView.as_view(), name="list"),
    path(
        "room/<uuid:chatname_room>/", 
        views.ChatRoomView.as_view(), 
        name="chat-room"
    )
]
