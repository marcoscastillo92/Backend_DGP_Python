from django.db import models
from users.models import User
from ckeditor.fields import RichTextField
# Create your models here.



class Groups(models.Model):
    name= models.CharField(max_length=150, verbose_name="Nombre")
    memberCount= models.IntegerField(default=0, verbose_name="Contador de miembros")
    users = models.ManyToManyField(User, verbose_name="Miembros", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Creado en", blank=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return f"{self.name}"

"""  
         def save(self, *args, **kwargs):
            
        usersRegistredAlready = Groups.objects.getUsers()
        notificacion = True
        for user in users:
            for uR in usersRegistredAlready:
                if user==uR:
                    notificacion = False
            if notificacion:
                print("Usuario agregado ")
                #pritnuser.Notify("Grupo")
        super(Groups, self).save(*args, **kwargs)
 """


class MessageForumGroup(models.Model):
    body = RichTextField(verbose_name="Mensaje")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    mimeType = models.FileField(upload_to ='uploads/attach', default="null", verbose_name="Tipo de mensaje") 
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, verbose_name="Grupo")
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha de creacion")

    def save(self, *args, **kwargs):
        super(MessageForumGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"