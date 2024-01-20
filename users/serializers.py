from proposals.models import ProposalPost
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from users.models import Job, Role


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
    job = JobSerializer(required=False)
    role = RoleSerializer(required=False)
    division = serializers.SerializerMethodField(required=False)
    department = serializers.SerializerMethodField(required=False)
    office = serializers.SerializerMethodField(required=False)
   
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

   
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'phone_number', 'telegram', 'firstname', 'lastname', 
                  'surname', 'birthday', 'job', 'role', 'division', 'department', 'office')
