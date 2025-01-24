from rest_framework import serializers
from database.models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = "__all__"