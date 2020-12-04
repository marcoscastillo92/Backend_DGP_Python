from django.db import models
from datetime import datetime
import json
import secrets
from django.contrib.auth.models import User as Tutor
from ckeditor.fields import RichTextField

def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    #Error al crear un nuevo usuario, instance.id -> None ¿usar secrets?
    return 'static/uploads/img/user_{0}/{1}'.format(instance.id, filename)

def pictogram_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'static/uploads/img/pictograms/{1}'.format(instance.username, filename)
def generateToken():
    return secrets.token_hex(64)

class User(models.Model):
    class Gender(models.TextChoices):
        male = 'male',
        female = 'female'

    name= models.CharField(verbose_name=("Nombre y Apellidos"), max_length=150)
    email= models.CharField(verbose_name=("Correo Electrónico"), max_length=150)
    username= models.CharField(verbose_name=("Nombre de Usuario"), max_length=150)
    password= models.CharField(verbose_name=("Contraseña"), max_length=150)
    phoneNumber= models.CharField(verbose_name=("Número de Teléfono"), max_length=150)
    profileImage= models.ImageField(verbose_name=("Imagen de Perfil"), upload_to=user_directory_path, blank=True)
    birthDate= models.DateTimeField(verbose_name=("Fecha de Nacimiento"), auto_now_add=True)
    token= models.CharField(max_length=300, default="null")
    gender= models.CharField(verbose_name=("Sexo"), max_length=6, choices=Gender.choices, default=Gender.male)
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
    image= models.ImageField(verbose_name=("Imagen de Pictograma"), upload_to=pictogram_directory_path, default='null')

