from django.db import models
from datetime import datetime
import json
import secrets

def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'uploads/img/user_{0}/{1}'.format(instance.user.id, filename)

class User(models.Model):
    """ class Role(models.TextChoices):
        admin = 'admin',
        tutor = 'tutor',
        user = 'user', """

    class Gender(models.TextChoices):
        male = 'male',
        female = 'female'
    
    name= models.CharField(max_length=150)
    email= models.CharField(max_length=150)
    username= models.CharField(max_length=150)
    password= models.CharField(max_length=150)
    phoneNumber= models.CharField(max_length=150)
    profileImage= models.ImageField(upload_to=user_directory_path, default='null')
    role= models.CharField(max_length=5, choices=Role.choices, default=Role.tutor)
    birthDate= models.DateTimeField(auto_now_add=True)
    token= models.CharField(max_length=300)
    gender= models.CharField(max_length=6, choices=Gender.choices, default=Gender.male)
    createdAt= models.DateTimeField(default=datetime.now, blank=True)

 
    def __str__(self):
        return """
            Nombre: %s \n
            Username: %s \n
            phoneNumber: %s \n
           
            
        """ %(self.name, self.username,self.phoneNumber)
class Pictograms(models.Model):
    name= models.CharField(max_length=150)
    key= models.CharField(max_length=300)
    section= models.CharField(max_length=150)
