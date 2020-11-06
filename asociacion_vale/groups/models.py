from django.db import models
from datetime import datetime
from users.models import User

# Create your models here.
class Groups(models.Model):
    name= models.CharField(max_length=150)
    memberCount= models.IntegerField(default=0)
    category = models.CharField(max_length=150)
    users = models.ManyToManyField(User)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)