from django.db import models
from datetime import datetime
from django.contrib.auth.models import User as Tutor
from users.models import User
from ckeditor.fields import RichTextField

class Forum(models.Model):
    body = RichTextField(verbose_name="Mensaje")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name="Tutor")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    mimeType = models.FileField(upload_to ='uploads/attach', default="null", verbose_name="Tipo de mensaje") 
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creacion")
    category = models.CharField(verbose_name=("Categoria Mensaje"), max_length=200)
    identifier = models.CharField(verbose_name=("Identificador"),max_length=300)
    #Cada vez que se cree un grupo o una tarea se crea un Forum con un "identifier" asociado
    #Este "identifier" será fijo, todos lo smensajes asociados a un grupo o un tarea tendrán este ID

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
    
    def __str__(self):
        return self.category