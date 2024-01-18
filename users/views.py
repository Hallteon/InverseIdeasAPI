from rest_framework import generics, permissions
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CurrentUserAPIDetailView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        
        return Response(serializer.data)
    