from django.db import models

# Create your models here.
class User(models.Model):
    name= models.CharField(max_length=150)
    email= models.CharField(max_length=150)
    username= models.CharField(max_length=150)
    password= models.CharField(max_length=150)
    phoneNumber= models.CharField(max_length=150)
    profileImage= models.ImageField(default='null')
    #role= {type= String, enum= ['admin', 'tutor', 'user'], default= 'user'}
    #birthDate= models.DateTimeField()
    token= models.CharField(max_length=300)
    createdAt= models.DateTimeField(auto_now_add=True)
    #gender= {type= String, enum= ['male', 'female'], default= 'male'}

class Pictograms(models.Model):
    name= models.CharField(max_length=150)
    key= models.CharField(max_length=300)
    section= models.CharField(max_length=150)
    value= models.CharField(max_length=150)


class Message(models.Model):
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
   # mimeType = 
    createdAt = models.DateTimeField(auto_now_add=True)
    
class Log(models.Model):
    source = models.CharField(max_length=150),
    message = models.CharField(max_length=150),
    data = models.Field
    createdAt = models.DateTimeField(auto_now_add=True)

class Groups(models.Model):
    name= models.CharField(max_length=150)
    memberCount= models.IntegerField
    category = models.CharField(max_length=150)
   # users = models.ma
    createdAt = models.DateTimeField(auto_now_add=True)


class Forum (models.Model):
    idTarget = models.ForeignKey(Groups, on_delete=models.CASCADE)
    #messages
    createdAt = models.DateTimeField(auto_now_add=True)
