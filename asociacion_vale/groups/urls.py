from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.groupsCreate, name='groupsCreate'),
    path('get' , views.groupsGet, name='groupsGet'),
    path('delete' , views.groupsDelete, name='groupsDelete'),
    path('post-message',views.groupsPostMessage, name='groupsPostMessage'),
]