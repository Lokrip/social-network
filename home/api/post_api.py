from django.db.models import (
    Case, 
    When, 
    Value, 
    Count,
    CharField,
)

from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.parsers import (
    MultiPartParser,
    FileUploadParser,
)

from home.serializers.post_serializers import (
    PostListSerializer,
    PostCreateSerializer,
    PostCreateImageSerializer,
    PostCreateVideoSerializer
)

from database.models import Post, PostTags


class CreatePostView(ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [
        MultiPartParser, 
        FileUploadParser,
    ]
    
    """
    ViewSet for creating posts.
    """
    def create(self, request):

        video = request.FILES.getlist('video')
        image_file = request.FILES.getlist('images_file')
        
        if image_file and len(image_file):
            serializer = PostCreateImageSerializer(data=request.data, context={'request': request})
        elif video and len(video):
            serializer = PostCreateVideoSerializer(data=request.data, context={'request': request})
        else:
            serializer = PostCreateSerializer(data=request.data, context={'request': request})
            
        if serializer.is_valid():
            serializer.save()
            return Response({
                'post': serializer.data, 
                'status': 'redirect'
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostListApi(APIView):
    def get(self, request):
        post = Post.objects.prefetch_related(
            "user",
            "product_images",
            "product_video"
        ).order_by('-pk').annotate(
            image_count=Count("product_images"),
            postType=Case(
                When(product_video__video__isnull=False, then=Value("video")),
                When(image_count=1, then=Value("image")),
                When(image_count__gt=1, then=Value("multi-image")),
                default=Value("unknown"),
                #Задает тип возвращаемого значения например multi-image это строка так что используем CharField
                output_field=CharField()
            )
        )
        
        paginator = PostListPagination()
        paginated_posts = paginator.paginate_queryset(post, request, view=self)
        serializer = PostListSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)