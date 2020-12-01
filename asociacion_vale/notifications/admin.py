from django.contrib import admin
from .models import Notifications

class NotificationsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Notifications)