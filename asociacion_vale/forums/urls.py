from django.urls import path
from . import views


urlpatterns = [
    path('post-message/', views.postMessage, name='postMessage'),
]