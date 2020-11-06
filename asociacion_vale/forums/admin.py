from django.contrib import admin
from .models import Forum, Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_filter = ('forum', 'author__username', 'createdAt')
    pass

class ForumAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)
admin.site.register(Forum, ForumAdmin)