from django.db import models
from datetime import datetime
from users.models import User
from groups.models import Groups
from ckeditor.fields import RichTextField

# Create your models here.
class Forum (models.Model):
    name = models.CharField(max_length=150)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"

    def __str__(self):
        return "Chat de "+str(self.idTarget)

class Message(models.Model):
    body = RichTextField(verbose_name="Contenido")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    mimeType = models.FileField(upload_to ='uploads/attach', default="null") 
    forum = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if self.forum is None:  # Set default reference
            self.forum = Groups.objects.get(id=1)
        super(Message, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return str(self.id)+" - "+str(self.createdAt)+" - "+self.author.name+" | "+self.body