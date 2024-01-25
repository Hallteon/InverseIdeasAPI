from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Achievement, AchievementType, CustomUser
from users.serializers import AchievementSerializer, AchievementTypeSerializer, CustomUserSerializer


class CurrentUserAPIDetailView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        
        return Response(serializer.data)
    
    
class CurrentUserAPIUpdateView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
    
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    
        return Response(serializer.data)
    
    
class AchievementTypeAPIListView(generics.ListAPIView):
    queryset = AchievementType.objects.all()
    serializer_class = AchievementTypeSerializer
    permission_classes = [IsAuthenticated]    

    
class AchievementAPICreateView(generics.CreateAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    
class AchievementAPIListView(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    
    