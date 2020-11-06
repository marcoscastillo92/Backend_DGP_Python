from django.contrib import admin
from .models import Groups, Category

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    pass

class CategoriesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Groups, GroupsAdmin)

admin.site.register(Category, CategoriesAdmin)