from django.contrib import admin
from companies.models import *


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' ,  'description', 'creation_date', 'address')
    search_fields = ('id', 'name')
    list_filter = ('name', 'creation_date', 'address')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('id', 'name')
    list_filter = ('name',)
    

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)
    
    
admin.site.register(Office, OfficeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Division, DivisionAdmin)