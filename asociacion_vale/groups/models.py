from django.db import models
from datetime import datetime
from users.models import User

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
    users = models.ManyToManyField(User, verbose_name="Miembros")
    createdAt = models.DateTimeField(default=datetime.now, verbose_name="Creado en", blank=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        print(self.category)
        return f"{self.name} - {self.category}"

    def save(self, idCategory, *args, **kwargs):
        if self.category is None:  # Set default reference
            self.category = Category.objects.get(id=1)
        elif idCategory:
            self.category = Category.objects.get(id=idCategory)

        super(Groups, self).save(*args, **kwargs)