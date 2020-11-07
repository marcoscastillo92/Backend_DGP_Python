from django.contrib import admin
from .models import Forum, MessageForum

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_filter = ('forum', 'author__username', 'createdAt')
    pass

class ForumAdmin(admin.ModelAdmin):
    pass

admin.site.register(MessageForum, MessageAdmin)
admin.site.register(Forum, ForumAdmin)