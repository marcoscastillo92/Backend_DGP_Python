from django.db import models
from users.models import User

class Notifications(models.Model):
    messageTitle =  models.CharField( max_length=300)
    messageBody = models.CharField(verbose_name=("Cuerpo"), max_length=300)
    apiKey = models.CharField(verbose_name=("ApiKey"),  default="", max_length=300)
    user = models.ManyToManyField(User,verbose_name="Usuarios" , blank=True , related_name='Usuarios')

    def __str__(self):
        return f"{self.messageTitle}"