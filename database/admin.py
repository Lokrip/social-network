from django.contrib import admin
from .models import (
    User, 
    Post,
    Story,
    PostTags, 
    PostVideo,
    PostImages,
    Notification,
    Friendship,
    GroupMessage,
    ChatGroup,
    GenerateCodeConfirmationEmail
)

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Story)
admin.site.register(PostTags)
admin.site.register(PostVideo)
admin.site.register(PostImages)
admin.site.register(Notification)
admin.site.register(Friendship)
admin.site.register(GroupMessage)
admin.site.register(ChatGroup)
admin.site.register(GenerateCodeConfirmationEmail)
