from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.usersCreate, name='usersCreate'),
    path('login' , views.usersLogin, name='usersLogin' ),
    path('randomUser', views.randomUser, name='randomUser'),
    path('generatePassword', views.generatePassword, name='generatePassword'),
    path('pictograms', views.pictograms, name='pictograms'),
    path('profile', views.profile, name="profile"),
    path('logout', views.logout, name="logout")

]