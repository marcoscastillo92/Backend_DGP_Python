from django.contrib import admin
from .models import Groups, MessageForumGroup, ForumGroup

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    pass


class MessageForumGroupAdmin(admin.ModelAdmin):
    
    list_display = ("author", "body" , "createdAt", "group")
    search_fields = ["author__name" ,"createdAt" , "group__name"]


admin.site.register(MessageForumGroup, MessageForumGroupAdmin)
admin.site.register(Groups, GroupsAdmin)

