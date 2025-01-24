from rest_framework import serializers
from database.models import (
    User,
    PostVideo,
    PostImages
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'image')

class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ('id', 'image',)
        
    # Метод to_representation в Django REST Framework 
    # (DRF) используется для управления процессом преобразования
    # объектов модели в их сериализованные представления (например, JSON). 
    # Этот метод вызывается при сериализации данных, то есть 
    # когда данные модели нужно подготовить для отправки клиенту
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     print(representation, instance)
    #     if not instance.image:
    #         representation['image'] = static("images/default-image.png")
    #     return representation
        
class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ('id', 'video', "video_image",)