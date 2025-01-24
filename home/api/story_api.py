import base64
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from database.models import Story

from home.serializers.story_serializers import (
    StorySerializer,
    StoryCreateImageSerializer,
    StoryCreateVideoSerializer,
)

class CreateStoryView(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """
        ViewSet for creating posts.
        """ 
        video_story_file = request.FILES.get("video_story_file")
        image_story_file = request.FILES.get("image_story_file")
        # print(image_story_file, video_story_file, request.data)
        
        # print(image_story_file, request.data)
        
        if image_story_file:
            serializer = StoryCreateImageSerializer(data=request.data, context={'request': request})
        elif video_story_file:
            serializer = StoryCreateVideoSerializer(data=request.data, context={'request': request})
        else:
            return Response({'error': "Upload a video or image"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'story': serializer.data,
                'status': "redirect"
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class StoryApi(ViewSet):
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "Without an identifier it is impossible to obtain data"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            decoded_id = base64.urlsafe_b64decode(pk).decode()
        except (base64.binascii.Error, ValueError):
            return Response(
                {"error": "Invalid identifier"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        story = get_object_or_404(Story, pk=decoded_id)
        serializer = StorySerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
        