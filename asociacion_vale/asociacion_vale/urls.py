"""asociacion_vale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from asociacion_vale.views import tutorsLogin
from django.contrib import admin
from django.urls import path, include
#from pictograms import views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tutors/home' , views.tutorsHome , name='home'),
    path('tutors/groups' , views.tutorsGroup , name='groups'),
    path('tutors/users' , views.tutorsUsers , name='users'),
    path('tutors/login' , views.tutorsLogin, name='login' ),
    path('tutors/logout' , views.tutorsLogout , name='logout'),
    path('tutors/groups/chat' , views.groupsChat, name='groupsChat'),
    path('tutors/groups/chat/post-message' , views.groupsChat, name='groupsChat'),
    path('tutors/groups/edit' , views.groupsEdit, name='groupsEdit'),
    path('tutors/groups/edit/confirm' , views.groupsEditConfirm, name='groupsEditConfirm'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
    path('tasks/', include('tasks.urls')),
    path('post-message', views.postMessage, name='postMessage'),
    path('get-messages', views.getMessages, name="getMessages"),
]
