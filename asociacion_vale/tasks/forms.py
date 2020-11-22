from django import forms
from tasks.models import Category
from users.models import User
from ckeditor import fields


class TaskForm(forms.Form):
    title = forms.CharField(label='Título', max_length=200)
    shortDescription = forms.CharField(label='Descripción corta', max_length=600)
    fullDescription = fields.RichTextFormField()
    image = forms.ImageField(allow_empty_file=True)
    media = forms.FileField(allow_empty_file=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), initial=0)
