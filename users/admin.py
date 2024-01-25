from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import *


class AchievementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'points', 'achievement_type_name', 'cover')
    search_fields = ('id', 'name', 'description')
    list_filter = ('points',)


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'achievement_type',  'current_progress', 'total_progress')
    search_fields = ('id', 'total_progress')
    list_filter = ('current_progress', 'total_progress')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type')
    search_fields = ('id', 'name', 'role_type')
    list_filter = ('name', 'role_type')
    
    
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'avatar', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'avatar', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'avatar', 'password1', 'password2'),
        }),)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementType, AchievementTypeAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)


