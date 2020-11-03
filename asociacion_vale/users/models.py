from django.db import models

# Create your models here.
class User(models.Model):
    name= models.CharField(max_length=150)
    email= models.CharField(max_length=150)
    username= models.CharField(max_length=150)
    password= models.CharField(max_length=150)
    phoneNumber= models.CharField(max_length=150)
    profileImage= models.ImageField(default='null')
    role= {type= String, enum= ['admin', 'tutor', 'user'], default= 'user'}
    birthDate= models.DateTimeField()
    token= models.CharField(max_length=300)
    createdAt= models.DateTimeField(auto_now_add=True)
    gender= {type= String, enum= ['male', 'female'], default= 'male'}