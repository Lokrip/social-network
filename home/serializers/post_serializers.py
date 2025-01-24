from django.templatetags.static import static
from appSerilizers.serializers import (
    UserSerializer,
    PostVideoSerializer,
    PostImagesSerializer
)

from rest_framework import serializers
from database.models import (
    Post,
    User,
    PostVideo,
    PostImages
)


class PostListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    postType = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    product_video = PostVideoSerializer()
    
    def get_postType(self, instance):
        return instance.postType
    
    def get_product_images(self, instance):
        images = instance.product_images.all()
        if not images.exists():
            return {'id': None, 'image': static("images/default-image.png")}
        return PostImagesSerializer(images, many=True).data
    
    class Meta:
        model = Post
        fields = ("id", "user", "title", "content",
            "status", "views", "slug", "postType",
            "product_images", "product_video"
        )


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("user", "title", "content")

    def validate_title(self, value):
        """Проверка на минимальную длину заголовка."""
        if not value.strip():
            raise serializers.ValidationError("Заголовок не может быть пустым.")
        if len(value) < 5:
            raise serializers.ValidationError("Заголовок должен содержать минимум 5 символов.")
        return value

    def validate_content(self, value):
        """Проверка на недопустимое содержимое."""
        forbidden_words = ["хуй", "даун"]
        for word in forbidden_words:
            if word in value:
                raise serializers.ValidationError(f"Содержимое содержит недопустимое слово: {word}")
        return value

    def validate(self, attrs):
        """Общая проверка: заголовок и содержимое не должны совпадать."""
        if attrs["title"] == attrs["content"]:
            raise serializers.ValidationError("Заголовок и содержимое не должны быть одинаковыми.")
        return attrs
        
        
class PostCreateImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images_file = serializers.ListField(
        child=serializers.ImageField(required=False),
        required=False,
    )

    class Meta:
        model = Post
        fields = ("user", "title", "content", "images_file")
    
    def create(self, validated_data):
        images_file = validated_data.pop('images_file', None)
        post = Post.objects.create(**validated_data)

        # Handle images only if they exist
        if images_file:
            for file in images_file:
                PostImages.objects.create(
                    post=post,
                    image=file
                )
        return post
    
    
class PostCreateVideoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    video = serializers.ListField(
        child=serializers.FileField(required=False),
        required=False,
    )

    class Meta:
        model = Post
        fields = ("user", "title", "content", "video")
    
    def create(self, validated_data):
        video = validated_data.pop('video', None)
        post = Post.objects.create(**validated_data)

        # Handle video if it exists
        if video:
            for file in video:
                PostVideo.objects.create(
                    post=post,
                    video=file
                )

        return post