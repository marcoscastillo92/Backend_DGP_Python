from django.db import models
from datetime import datetime
from django.contrib.auth.models import User as Tutor
from users.models import User
from ckeditor.fields import RichTextField

class Forum(models.Model):
    body = RichTextField(verbose_name="Mensaje")
    emisorTutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name="Emisor Tutor", related_name='emisorTutor')
    emisorUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Emisor Usuario", related_name='emisorUser')
    receptorTutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name="Receptor Tutor", related_name='receptorTutor')
    receptorUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Receptor Usuario", related_name='receptorUser')
    
    mimeType = models.CharField(verbose_name="Tipo de mensaje", max_length=100, default="")
    path = models.CharField(verbose_name="Ruta", max_length=500, default=None)
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creacion")
    category = models.CharField(verbose_name=("Categoria Mensaje"), max_length=200)
    identifier = models.CharField(verbose_name=("Identificador"),max_length=300)
    #Cada vez que se cree un grupo o una tarea se crea un Forum con un "identifier" asociado
    #Este "identifier" será fijo, todos lo smensajes asociados a un grupo o un tarea tendrán este "identifier"


    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
    
    def __str__(self):
        return self.category

    def save_model(self, request, obj, form, change):
        if not change:
            obj.emisorTutor = request.user
        obj.save()