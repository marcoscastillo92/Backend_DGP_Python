from django.contrib import admin
from users.models import User , ForumUser, MessageForumUser



# Register your models here.

class ForumUserAdmin(admin.ModelAdmin):
    list_display = ("user", "tutor" , "createdAt")
    search_fields = ["user__username" ,"tutor__username", "createdAt" ]
class MessageForumUserAdmin(admin.ModelAdmin):
    
    list_display = ("author", "body" , "createdAt", "forum")
    search_fields = ["author__username" ,"createdAt" , "forum__tutor__username"]

admin.site.register(User)
admin.site.register(ForumUser,ForumUserAdmin)
admin.site.register(MessageForumUser, MessageForumUserAdmin)