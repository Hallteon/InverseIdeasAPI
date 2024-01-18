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
        fields = ('id', 'name', 'author', 'category', 'level', 'content', 'document', 'histories', 'created_date')