from django.contrib import admin
from .models import Task, Progress, Rating, Category

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    pass

class ProgressAdmin(admin.ModelAdmin):
    pass

class RatingAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Category, CategoryAdmin)