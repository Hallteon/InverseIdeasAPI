from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import *


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
    list_display = ('id', 'email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'telegram', 'firstname', 'lastname', 'surname', 'birthday', 'job', 'role', 'password1', 'password2'),
        }),)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Job, JobAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)

