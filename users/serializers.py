from proposals.models import Proposal, ProposalPost
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from users.models import *


class AchievementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementType
        fields = ('id', 'name', 'cover', 'description', 'points')


class AchievementSerializer(serializers.ModelSerializer):
    achievement_type = AchievementTypeSerializer(required=False)
    
    class Meta:
        model = Achievement
        fields = ('id', 'achievement_type', 'current_progress','total_progress')


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
        
        
class CustomUserAnalyticsSerializer(serializers.ModelSerializer):
    job = JobSerializer(required=False)
    role = RoleSerializer(required=False)
    likes = serializers.SerializerMethodField(required=False)
    views = serializers.SerializerMethodField(required=False)
   
    def get_views(self, obj):
        try:
            num_views = 0
            
            for post in ProposalPost.objects.filter(proposal__author=obj).distinct():
                num_views += post.views
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_views
   
    def get_likes(self, obj):
        try:
            num_likes = 0
        
            for post in ProposalPost.objects.filter(proposal__author=obj).distinct():
                num_likes += post.likes
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
   
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'phone_number', 'telegram', 'firstname', 'lastname', 
                  'surname', 'birthday', 'job', 'role', 'likes', 'views')


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    job = JobSerializer(required=False)
    role = RoleSerializer(required=False)
    achievements = AchievementSerializer(required=False, many=True)
    division = serializers.SerializerMethodField(required=False)
    department = serializers.SerializerMethodField(required=False)
    office = serializers.SerializerMethodField(required=False)
    likes_sended = serializers.SerializerMethodField(required=False)
    proposals = serializers.SerializerMethodField(required=False)
    achievements_count = serializers.SerializerMethodField(required=False)
    achievements_points = serializers.SerializerMethodField(required=False)
   
    def get_division(self, obj):
        try:
            division_name = obj.divisions_employee.all().get().name
        except ObjectDoesNotExist as e:
            return None
        else:
            return division_name
        
    def get_department(self, obj):
        try:
            division_data = obj.divisions_employee.all().get()
            department_name = division_data.departments_division.all().get().name
        except ObjectDoesNotExist as e:
            return None
        else:
            return department_name
    
    def get_office(self, obj):
        try:
            division_data = obj.divisions_employee.all().get()
            department_data = division_data.departments_division.all().get()
            office_name = department_data.offices_department.all().get().name
        except ObjectDoesNotExist as e:
            return None
        else:
            return office_name
        
    def get_likes_sended(self, obj):
        try:
            num_likes = 0
            
            for post in ProposalPost.objects.filter(likes__id=obj.id).distinct():
                num_likes += 1
            
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
        
    def get_proposals(self, obj):
        num_proposals = Proposal.objects.filter(author=obj).count()

        return num_proposals
    
    def get_achievements_count(self, obj):
        num_achievements = obj.achievements.count()
        
        return num_achievements
    
    def get_achievements_points(self, obj):
        achievements_points = 0
        
        for achievement in obj.achievements.all():
            achievements_points += achievement.points
        
        return achievements_points
   
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'avatar', 'phone_number', 'telegram', 'firstname', 'lastname', 
                  'surname', 'birthday', 'job', 'role', 'achievements', 'achievements_count', 'achievements_points', 'likes_sended', 'proposals', 'division', 'department', 'office')
