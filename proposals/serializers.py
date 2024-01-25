from rest_framework import serializers
from proposals.models import *
from users.serializers import CustomUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'status_type')


class HistorySerializer(serializers.ModelSerializer):
    by_user = CustomUserSerializer(required=False)
    status = StatusSerializer(required=False)
    
    class Meta:
        model = History
        fields = ('id', 'by_user', 'status', 'date', 'comment')


class ProposalSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(required=False)
    histories = HistorySerializer(required=False, many=True)
    category = CategorySerializer(required=False)
    
    class Meta:
        model = Proposal
        fields = ('id', 'name', 'author', 'category', 'description', 'level', 'content', 'document', 'histories', 'created_date')
        
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        
        
class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(required=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_datetime')
        
        
class ProposalPostReadDetailSerializer(serializers.ModelSerializer):
    proposal = ProposalSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    comments = CommentSerializer(required=False, many=True)
    likes = serializers.SerializerMethodField(required=False)
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = ProposalPost
        fields = ('id', 'proposal', 'tags', 'comments', 'likes', 'views')       
        
        
class ProposalPostReadListSerializer(serializers.ModelSerializer):
    proposal = ProposalSerializer(required=False)
    likes = serializers.SerializerMethodField(required=False)
    comments = serializers.SerializerMethodField(required=False)
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_comments(self, obj):
        return obj.comments.count()
    
    class Meta:
        model = ProposalPost
        fields = ('id', 'proposal', 'tags', 'comments', 'likes', 'views')        
        
        
class ProposalPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalPost
        fields = ('id', 'proposal', 'tags', 'comments', 'likes', 'views')