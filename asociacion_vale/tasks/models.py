from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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

    class Status(models.TextChoices):
        ASSIGNED = 'assigned',
        DONE = 'done'

    title = models.CharField(verbose_name=("Título"), max_lenght=200)
    shortDescription = models.CharField(verbose_name=("Descripción corta"), max_lenght=600)
    fullDescription = RichTextField(verbose_name=("Descripción completa"))
    image = models.ImageField(verbose_name=("Icono"), upload_to=taskImageDirectoryPath, default='null')
    date = models.DateTimeField(verbose_name=("Fecha"), auto_now_add=True)
    media = models.FileField(verbose_name=("Archivo"), upload_to=taskMediaDirectoryPath, default='null')
    status = models.CharField(verbose_name=("Estado"), choices=Status.choices, default=Status.ASSIGNED)
    category = models.ForeignKey(Category, verbose_name=("Categoría"), on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.category is None:
            self.category = Category.objects.get(id=1)
        super(Task, self).save(*args, **kwargs)

class Rating(models.Model):
    task = models.ForeignKey(Task, verbose_name=("Tarea"), on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, verbose_name=("Usuario"), on_delete=models.CASCADE, null=True)
    text = models.CharField(verbose_name=("Opinion"), max_lenght=800)
    difficulty = models.IntegerField(verbose_name=("Dificultad"), default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    utility = models.IntegerField(verbose_name=("Utilidad"), default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if self.task is None:
            self.task = Task.objects.get(id=1)
        if self.user is None:
            self.user = User.objects.get(id=1)
        super(Rating, self).save(*args, **kwargs)

class Progress(models.Model):
    user = models.ForeignKey(User, verbose_name=("Usuario"), on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name=("Categoría"), on_delete=models.CASCADE, null=True)
    total = models.IntegerField(verbose_name=("Total"), default=0)
    done = models.IntegerField(verbose_name=("Completadas"), default=0)