from django.db import models
from datetime import datetime
from users.models import User
from ckeditor.fields import RichTextField
# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=200, verbose_name="Nombre")
    createdAt = models.DateTimeField(default=datetime.now, verbose_name="Creado en", blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Groups(models.Model):
    name= models.CharField(max_length=150, verbose_name="Nombre")
    memberCount= models.IntegerField(default=0, verbose_name="Contador de miembros")
    category = models.ForeignKey(Category, verbose_name=("Categoría"), on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(User, verbose_name="Miembros", blank=True)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name="Creado en", blank=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        print(self.category)
        return f"{self.name} - {self.category}"

    def save(self, *args, **kwargs):
        if self.category is None:  # Set default reference
            self.category = Category.objects.get(id=1)
        super(Groups, self).save(*args, **kwargs)

class ForumGroup (models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    Group =  models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, verbose_name="Grupo")
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Chat de Grupo"
        verbose_name_plural = "Chats de Grupo"

    def __str__(self):
        return str(self.name)

class MessageForumGroup(models.Model):
    body = RichTextField(verbose_name="Mensaje")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    mimeType = models.FileField(upload_to ='uploads/attach', default="null", verbose_name="Tipo de mensaje") 
    forum = models.ForeignKey(ForumGroup, on_delete=models.CASCADE, null=True, verbose_name="Foro")
    createdAt = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de creacion")

    def save(self, *args, **kwargs):
        if self.forum is None:  # Set default reference
            self.forum = Groups.objects.get(id=1)
        super(MessageForumGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"