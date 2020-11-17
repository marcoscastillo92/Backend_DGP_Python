from django.contrib import admin
from .models import Groups

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    pass




admin.site.register(Groups, GroupsAdmin)

