from django.contrib import admin
from .models import Groups, Category, MessageForumGroup, ForumGroup

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    pass

class CategoriesAdmin(admin.ModelAdmin):
    pass

class MessageForumGroupAdmin(admin.ModelAdmin):
    
    list_display = ("author", "body" , "createdAt", "forum")
    search_fields = ["author__name" ,"createdAt" , "forum__name"]


admin.site.register(ForumGroup)
admin.site.register(MessageForumGroup, MessageForumGroupAdmin)
admin.site.register(Groups, GroupsAdmin)

admin.site.register(Category, CategoriesAdmin)