from django.contrib import admin
from .models import Forum

# Register your models here.
class ForumsAdmin(admin.ModelAdmin):
    pass




admin.site.register(Forum, ForumsAdmin)

