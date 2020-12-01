from django.db import models
from users.models import User
from django.contrib.auth.models import User as Tutor
from forums.models import Forum
from ckeditor.fields import RichTextField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
import secrets
# Create your models here.

class Groups(models.Model):
    name= models.CharField(max_length=150, verbose_name="Nombre")
    memberCount= models.IntegerField(default=0, verbose_name="Contador de miembros")
    users = models.ManyToManyField(User, verbose_name="Miembros", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Creado en", blank=True)
    identifier = models.CharField(verbose_name=("Identificador"), default=secrets.token_hex(10), max_length=300),
    tutors = models.ManyToManyField(Tutor, verbose_name="Tutores", blank=True , related_name='tutores'),
    deviceToken = models.CharField(verbose_name=("TokenDispositivo"), default="", max_length=300)
    #Cada vez que se cree un grupo o una tarea se crea un Forum con un "identifier" asociado
    #Este "identifier" será fijo, todos lo smensajes asociados a un grupo o un tarea tendrán este "identifier"

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

@receiver(m2m_changed, sender=Groups.users.through)
def my_handler(sender, instance, **kwargs):
    group = Groups.objects.filter(id=instance.id)
    identifier = group[0].identifier
    isForumCreated = Forum.objects.filter(identifier=identifier)
    if not isForumCreated:
        forum = Forum(
            body = "Bienvenidos al chat de Grupo",
            emisorTutor = Tutor.objects.get(id=1), #obtener el tutor en la sesión
            emisorUser = None,
            receptorTutor = None, 
            receptorUser = None,
            category = "welcomeMessage",
            identifier = identifier
        )
        forum.save()