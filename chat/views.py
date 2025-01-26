from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin

from database.models import (
    ChatGroup,
    GroupMessage
)

class ChatListView(LoginRequiredMixin, View):
    def get(self, request):
        messagesGroup = ChatGroup.objects.filter(members=request.user)

        context = {
            'title': "Messages",
            'messagesGroup': messagesGroup
        }
        return render(request, "chat/chat-list.html", context)


class ChatRoomView(LoginRequiredMixin, View):
    def get(self, request, chatname_room):
        chat_group = get_object_or_404(ChatGroup, group_name=chatname_room)
        messages = GroupMessage.objects.filter(group=chat_group).reverse()

        context = {
            'title': chatname_room,
            'messages': messages,
            "chatname_room": chatname_room
        }
        return render(request, "chat/chat-room.html", context)
