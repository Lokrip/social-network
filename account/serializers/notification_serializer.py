from rest_framework import serializers
from database.models import (
    Notification,
)

from appSerilizers.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()
    
    class Meta:
        model = Notification
        fields = '__all__'
        