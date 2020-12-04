from django import forms
from tasks.models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'shortDescription', 'fullDescription', 'image', 'media', 'category', 'users']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']