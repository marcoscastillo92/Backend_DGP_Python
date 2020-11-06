from django.db import models
from datetime import datetime
from groups.models import Groups
from users.models import User

# Create your models here.
class Forum (models.Model):
    idTarget = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if self.idTarget is None:  # Set default reference
            self.idTarget = Groups.objects.get(id=1)
        super(Forum, self).save(*args, **kwargs)

class Message(models.Model):
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    mimeType = models.FileField(upload_to ='uploads/attach', default="null") 
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if self.forum is None:  # Set default reference
            self.forum = Forum.objects.get(id=1)
        super(Message, self).save(*args, **kwargs)
