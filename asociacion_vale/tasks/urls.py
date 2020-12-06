from django.urls import path
from . import views


urlpatterns = [
    path('create', views.createTask, name='createTask'),
    path('get' , views.getAllTasks, name='getTasks'),
    path('get/<int:id>' , views.getTask, name='getTask'),
    path('rate/' , views.rateTask, name='rateTask'),
    path('delete/<int:id>', views.deleteTask, name='deleteTask'),
    path('randomTask', views.randomTask, name='randomTask'),
    path('status', views.statusTask, name='statusTask'),
    path('progress', views.progressUser, name='progress'),
]