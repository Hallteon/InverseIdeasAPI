from companies.models import *
from proposals.models import Proposal, ProposalPost
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from users.serializers import *


class DivisionReadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ('id', 'name')
        

class DivisionSerializer(serializers.ModelSerializer):
    heads = CustomUserSerializer(required=False, many=True)
        
    class Meta:
        model = Division
        fields = ('id', 'name', 'employees', 'heads')


class DivisionAnalyticsSerializer(serializers.ModelSerializer):
    employees = CustomUserAnalyticsSerializer(required=False, many=True)
    heads = CustomUserSerializer(required=False, many=True)
    likes = serializers.SerializerMethodField(required=False)
    views = serializers.SerializerMethodField(required=False)
    proposals = serializers.SerializerMethodField(required=False)
        
    def get_views(self, obj):
        try:
            num_views = 0
            
            for employee in obj.employees.all():
                for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                    num_views += post.views
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_views
   
    def get_likes(self, obj):
        try:
            num_likes = 0
        
            for employee in obj.employees.all():
                for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                    num_likes += post.likes
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
        
    def get_proposals(self, obj):
        try:
            num_proposals = 0
            
            for employee in obj.employees.all():
                num_proposals += Proposal.objects.filter(author=employee).count()
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_proposals
        
    class Meta:
        model = Division
        fields = ('id', 'name', 'employees', 'heads', 'likes', 'views', 'proposals')


class DepartmentSerializer(serializers.Serializer):
    heads = CustomUserSerializer(required=False, many=True)
    divisions = DivisionSerializer(required=False, many=True)
    
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'heads', 'divisions')
        
class DepartmentAnalyticsSerializer(serializers.Serializer):
    heads = CustomUserSerializer(required=False, many=True)
    divisions = DivisionAnalyticsSerializer(required=False, many=True)
    likes = serializers.SerializerMethodField(required=False)
    views = serializers.SerializerMethodField(required=False)
    proposals = serializers.SerializerMethodField(required=False)
    
    def get_views(self, obj):
        try:
            num_views = 0
            
            for division in obj.divisions.all():
                for employee in division.employees.all():
                    for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                        num_views += post.views
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_views
   
    def get_likes(self, obj):
        try:
            num_likes = 0
            
            for division in obj.divisions.all():
                for employee in division.employees.all():
                    for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                        num_likes += post.likes
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
        
    def get_proposals(self, obj):
        try:
            num_proposals = 0
            
            for division in obj.divisions.all():
                for employee in division.employees.all():
                    num_proposals += Proposal.objects.filter(author=employee).count()
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_proposals
    
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'heads', 'divisions',
                  'likes', 'views', 'proposals')
        
        
class OfficeSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(required=False, many=True)
    heads = CustomUserSerializer(required=False, many=True)
    
    class Meta:
        model = Office
        fields = ('id', 'name', 'description', 'creation_date', 'address', 'heads',
                  'departments')
        
        
class OfficeAnalyticsSerializer(serializers.ModelSerializer):
    departments = DepartmentAnalyticsSerializer(required=False, many=True)
    heads = CustomUserSerializer(required=False, many=True)
    likes = serializers.SerializerMethodField(required=False)
    views = serializers.SerializerMethodField(required=False)
    proposals = serializers.SerializerMethodField(required=False)
    
    def get_views(self, obj):
        try:
            num_likes = 0
            
            for department in obj.departments.all():
                for division in department.divisions.all():
                    for employee in division.employees.all():
                        for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                            num_likes += post.views
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
   
    def get_likes(self, obj):
        try:
            num_likes = 0
            
            for department in obj.departments.all():
                for division in department.divisions.all():
                    for employee in division.employees.all():
                        for post in ProposalPost.objects.filter(proposal__author=employee).distinct():
                            num_likes += post.likes
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_likes
        
    def get_proposals(self, obj):
        try:
            num_proposals = 0
            
            for department in obj.departments.all():
                for division in department.divisions.all():
                    for employee in division.employees.all():
                        num_proposals += Proposal.objects.filter(author=employee).count()
        
        except ObjectDoesNotExist as e:
            return None
        
        else:
            return num_proposals
    
    class Meta:
        model = Office
        fields = ('id', 'name', 'description', 'creation_date', 'address', 'heads',
                  'departments', 'likes', 'views', 'proposals')
        

class CompanySerializer(serializers.ModelSerializer):
    ceo = CustomUserSerializer(required=False)
    offices = OfficeSerializer(required=False, many=True)
    
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'inn', 'kpp', 'ogrn', 'address',
                  'created_date', 'scope', 'ceo', 'offices')