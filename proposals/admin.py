from django.contrib import admin
from proposals.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status_type')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'by_user', 'status', 'date', 'comment')
    search_fields = ('id', 'by_user', 'date')
    list_filter = ('date',)


class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'category', 'level', 'created_date', 'document')
    search_fields = ('id', 'name', 'category')
    list_filter = ('name',)
    
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)

    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_datetime')
    search_fields = ('id', 'author', 'content')
    list_filter = ('author',)
    
    
class ProposalPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposal', 'likes', 'views')
    search_fields = ('id', 'likes', 'views')
    list_filter = ('likes', 'views')
    

admin.site.register(Category, CategoryAdmin)    
admin.site.register(Status, StatusAdmin)
admin.site.register(History, HistoryAdmin)    
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ProposalPost, ProposalPostAdmin)