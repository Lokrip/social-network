from datetime import timedelta, datetime
from rest_framework import serializers
from database.models import Story
from home.tasks import deleting_story


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"

class StoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expires_at = serializers.DateTimeField(required=False)
    
    class Meta:
        model = Story
        fields = ("user", "text", "created_at",
                  "expires_at", "seen_by")
        
    def create(self, validated_data):
        seen_by = validated_data.pop('seen_by', None)
        story = Story.objects.create(**validated_data)
        if story: deleting_story.apply_async((story.pk,), countdown=86500)
        if seen_by:
            story.seen_by.set(seen_by)
        return story
        

class StoryCreateImageSerializer(StoryCreateSerializer):
    
    image_story_file = serializers.ImageField(required=False)
    
    class Meta:
        model = Story
        fields = ("user", "text", "created_at", "image_story_file", 
                  "expires_at", "seen_by")
        
    def create(self, validated_data):
        image_story_file = validated_data.pop("image_story_file", None)
        story = super().create(validated_data)
        
        if image_story_file:
            story.image = image_story_file
            story.save()
        return story
    
class StoryCreateVideoSerializer(StoryCreateSerializer):
    video_story_file = serializers.FileField(required=False)
    
    
    class Meta:
        model = Story
        fields = ("user", "text", "created_at", "video_story_file", 
                  "expires_at", "seen_by")
        
    def create(self, validated_data):
        video_story_file = validated_data.pop("video_story_file", None)
        story = super().create(validated_data)
        
        if video_story_file:
            story.video = video_story_file
            story.save()
        return story