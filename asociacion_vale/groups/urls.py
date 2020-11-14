from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.groupsCreate, name='groupsCreate'),
    path('get/<int:id>' , views.groupsGet, name='groupsGet')
]