from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.usersCreate, name='usersCreate'),
    path('login/' , views.usersLogin, name='usersLogin' ),
    path('randomUser/', views.randomUser, name='randomUser'),
    path('password/', views.generatePassword, name='generatePassword'),
    path('pictograms/', views.pictograms, name='pictograms'),
]