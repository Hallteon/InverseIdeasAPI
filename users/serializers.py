from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Job, Role


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # token['email'] = user.email
#         token['phone_number'] = user.phone_number

#         return token


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'description')
        
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'role_type')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    job = JobSerializer(required=False)
    role = RoleSerializer(required=False)    
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role')
