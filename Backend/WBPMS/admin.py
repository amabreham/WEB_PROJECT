from django.contrib import admin
from django.contrib.auth.models import Group
 

from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.register(User)
 
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
class CustomizedUserAdmin(UserAdmin):
    inlines = (ProfileInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)    
admin.site.unregister(Group)
 
 

 
        
