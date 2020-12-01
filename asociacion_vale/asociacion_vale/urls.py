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
from django.contrib import admin
from django.urls import path, include
#from pictograms import views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tutors/home' , views.tutorsHome , name='home'),
    path('tutors/login' , views.tutorsLogin, name='login' ),
    path('tutors/logout' , views.tutorsLogout , name='logout'),
    path('tutors/users' , views.tutorsUsers , name='users'),
    path('tutors/users/edit/<int:id>' , views.tutorsUsersEdit , name='tutorsUserEdit'),
    path('tutors/users/add' , views.tutorsUsersAdd , name='tutorsUsersAdd'),
    path('tutors/users/add/confirm' , views.tutorsUsersAddConfirm , name='tutorsUsersAddConfirm'),
    path('tutors/users/tutorsEditUsersPictograms' , views.tutorsEditUsersPictograms , name='tutorsEditUsersPictograms'),
    path('tutors/users/tutorsEditUserPassword/<int:id>' , views.tutorsEditUserPassword , name='tutorsEditUserPassword'),
    path('tutors/users/delete', views.tutorsUsersDelete, name="tutorsUsersDelete"),
    path('tutors/users/delete/<int:id>', views.tutorsUsersDeleteById, name="tutorsUsersDeleteById"),
    path('tutors/groups', views.tutorsGroup , name='groups'),
    path('tutors/groups/chat/get/<str:id>' , views.groupsGetChat, name='groupsGetChat'),
    path('tutors/groups/chat/post-message' , views.groupsPostMessage, name='tutorsGroupsPostMessage'),
    path('tutors/groups/edit/<str:id>' , views.groupsEdit, name='tutorsGroupsEdit'),
    path('tutors/groups/editConfirm' , views.groupsEditConfirm, name='groupsEditConfirm'),
    path('tutors/groups/create' , views.groupsCreate, name='tutorsGroupsCreate'),
    path('tutors/groups/createConfirm' , views.groupsCreateConfirm, name='groupsCreateConfirm'),
    path('tutors/home', views.tutorsHome, name='tutorHome'),
    path('tutors/groups', views.tutorsGroup, name='tutorGroups'),
    path('tutors/login', views.tutorsLogin, name='tutorLogin'),
    path('tutors/logout', views.tutorsLogout, name='tutorLogout'),
    path('tutors/tasks', views.tutorsTasks, name='tutorTasks'),
    path('tutors/tasks/create', views.tutorTasksCreate, name='tutorTasksCreate'),
    path('tutors/tasks/<int:id>', views.tutorsTasksDetail, name='tutorTasksEdit'),
    path('tutors/tasks/delete/<int:id>', views.tutorsTasksDelete, name='tutorTasksDelete'),
    path('tutors/tasks/chat/<str:identifier>', views.tasksChat, name='taskChat'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
    path('tasks/', include('tasks.urls')),
    path('post-message', views.postMessage, name='postMessage'),
    path('get-messages', views.getMessages, name="getMessages"),
]
