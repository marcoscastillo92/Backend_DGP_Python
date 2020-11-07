from django.db import models
from datetime import datetime
import json
import secrets
from django.contrib.auth.models import User as Tutor
from ckeditor.fields import RichTextField


def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'uploads/img/user_{0}/{1}'.format(instance.id, filename)
def generateToken():
    return secrets.token_hex(64)

class User(models.Model):
    class Gender(models.TextChoices):
        male = 'male',
        female = 'female'

    name= models.CharField(max_length=150)
    email= models.CharField(max_length=150)
    username= models.CharField(max_length=150)
    password= models.CharField(max_length=150)
    phoneNumber= models.CharField(max_length=150)
    profileImage= models.ImageField(upload_to=user_directory_path, default='null')
    birthDate= models.DateTimeField(auto_now_add=True)
    token= models.CharField(max_length=300, default=generateToken())
    gender= models.CharField(max_length=6, choices=Gender.choices, default=Gender.male)
    createdAt= models.DateTimeField(default=datetime.now, blank=True)

 
    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Pictograms(models.Model):
    name= models.CharField(max_length=150)
    key= models.CharField(max_length=300)
    section= models.CharField(max_length=150)


class ForumUser (models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Propietario")
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creación")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, verbose_name="Tutor")
    class Meta:
        verbose_name = "Chat de Usuario"
        verbose_name_plural = "Chats de Usuario"

    def __str__(self):
        return f"{self.tutor}"
class MessageForumUser(models.Model):
    body = RichTextField(verbose_name="Mensaje")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    mimeType = models.FileField(upload_to ='uploads/attach', default="null", verbose_name="Tipo de mensaje") 
    forum = models.ForeignKey(ForumUser, on_delete=models.CASCADE, null=True, verbose_name="Conversacion")
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creacion")

    def save(self, *args, **kwargs):
        if self.forum is None:  # Set default reference
            self.forum = ForumUser.objects.get(id=1)
        super(MessageForumUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"