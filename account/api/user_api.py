from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import AnonymousUser

from appSerilizers.serializers import UserSerializer

class UserApi(APIView):
    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({
                "id": None,
                "username": "Anonymous",
                "email": "Anonymous",
                "image": None 
            }, status=status.HTTP_200_OK)
            
        serializer = UserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )