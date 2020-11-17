from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from users.models import User
from forums.models import Forum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.serializers import serialize
from django.contrib.auth.models import User as Tutor
import secrets
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

def taskImageDirectoryPath(instance, filename): 
    return 'uploads/tasks/{0}/images/{1}'.format(instance.id, filename)
def taskMediaDirectoryPath(instance, filename): 
    return 'uploads/tasks/{0}/media/{1}'.format(instance.id, filename)

class Category(models.Model):
    title= models.CharField(max_length=200, verbose_name="Título")
    createdAt = models.DateTimeField(default=datetime.now, verbose_name="Creado en", blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.title

class Task(models.Model):

    title = models.CharField(verbose_name=("Título"), max_length=200)
    shortDescription = models.CharField(verbose_name=("Descripción corta"), max_length=600)
    fullDescription = RichTextField(verbose_name=("Descripción completa"))
    image = models.ImageField(verbose_name=("Icono"), upload_to=taskImageDirectoryPath, default='null')
    date = models.DateTimeField(verbose_name=("Fecha"), auto_now_add=True)
    media = models.FileField(verbose_name=("Archivo"), upload_to=taskMediaDirectoryPath, default='null')
    category = models.ForeignKey(Category, verbose_name=("Categoría"), on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(User, verbose_name="Asignada a", related_name="usuarios", blank=True)
    identifier = models.CharField(verbose_name=("Identificador"), default=secrets.token_hex(10), max_length=300)
    
    def save(self, *args, **kwargs):
        if self.category is None:
            self.category = Category.objects.get(id=1)

        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.shortDescription}'

    def serializeCustom(self, token):
        try:
            rating = Rating.objects.filter(task__id=self.id, user__token=token)[0]
            text = rating.text
            difficulty = rating.difficulty
            utility = rating.utility
        except:
            text = ""
            difficulty = 0
            utility = 0

        data = { 
                "id_tarea": self.id,
                "title": self.title,
                "shortDescription": self.shortDescription,
                "fullDescription": self.fullDescription.replace("\"", "	&quot;"),
                "image": self.image.url,
                "mediaDescription": self.media.path.replace("\\", "/").split("asociacion_vale/")[1],
                "category": str(self.category),
                "rating": {
                    "text": text,
                    "difficulty": difficulty,
                    "utility": utility
                }
            }
        return data

class Rating(models.Model):
    task = models.ForeignKey(Task, verbose_name=("Tarea"), on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, verbose_name=("Usuario"), on_delete=models.CASCADE, null=True)
    text = models.CharField(verbose_name=("Opinion"), max_length=800)
    difficulty = models.IntegerField(verbose_name=("Dificultad"), default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    utility = models.IntegerField(verbose_name=("Utilidad"), default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if self.task is None:
            self.task = Task.objects.get(id=1)
        if self.user is None:
            self.user = User.objects.get(id=1)
        super(Rating, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user} | {str(self.task).split("-")[0]} | Dificultad: {self.difficulty} | Utilidad: {self.utility} | Comentario: {self.text}'

class Progress(models.Model):
    user = models.ForeignKey(User, verbose_name=("Usuario"), on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name=("Categoría"), on_delete=models.CASCADE, null=True)
    total = models.IntegerField(verbose_name=("Total"), default=0)
    done = models.IntegerField(verbose_name=("Completadas"), default=0)

    def __str__(self):
        return f'{str(self.user)} | {str(self.category)} - {self.done}/{self.total}'


@receiver(m2m_changed, sender=Task.users.through)
def my_handler(sender, instance, **kwargs):
    tarea = Task.objects.filter(id=instance.id)
    identifier = tarea[0].identifier
    isForumCreated = Forum.objects.filter(identifier=identifier)
    if not isForumCreated:
        for user in tarea[0].users.all():
            forum = Forum(
                body = "Bienvenidos al chat de tarea",
                emisorTutor = Tutor.objects.get(id=1), #obtener el tutor en la sesión
                emisorUser = None,
                receptorTutor = None, 
                receptorUser = user,
                category = "welcomeMessage",
                identifier = identifier
            )
            forum.save()

#def usersTask():
    

#m2m_changed.connect(usersTask, sender=Task.users.through)
