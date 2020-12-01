from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .controller import Controller
from groups.controller import Controller as gController
from users.controller import Controller as uController
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def postMessage(request):
    if request.method == 'POST':
        controller = Controller()
        return controller.postMessage(request)


@csrf_exempt
def getMessages(request):
    if request.method == 'GET':
        controller = Controller()
        return controller.getMessages(request)


@csrf_exempt
def index(request):
    if request.session.get('username', False):
            return redirect('/tutors/home')
    else:
            
        if request.method == 'GET':
            return render(request, './tutors/index.html')


@csrf_exempt
def tutorsLogin(request):   
    if request.method == 'POST':
        controller = Controller()
        return controller.tutorLogin(request)


@csrf_exempt
def tutorsHome(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            return render(request, './tutors/home.html')
        else:
            return redirect('/')


@csrf_exempt
def tutorsLogout(request):
    
    # Borro la cookie de usurname que es la que me dice si estoy logueado
    del request.session['username']
    request.session.modified = True
    return redirect('/')


@csrf_exempt
def tutorsGroup(request):
    if request.session.get('username', False):
        if request.method == 'GET':
            controller = Controller()
            return  controller.tutorGroups(request)
    return redirect('/')
@csrf_exempt
def tutorsUsers(request):
    if request.session.get('username', False):

        if request.method == 'GET':
            controller = Controller()
            return  controller.tutorUsers(request)
    return redirect('/')
@csrf_exempt
def groupsEdit(request, id):
    if request.session.get('username', False):
        controller = gController()
        return controller.editGroup(request, id)
    return redirect('/')

@csrf_exempt
def groupsEditConfirm(request):
    if request.session.get('username', False):
        if request.method == 'POST':
           
            controller = gController()
            return controller.editConfirmGroup(request)
    return redirect('/')

@csrf_exempt
def groupsCreateConfirm(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            controller = gController()
            return controller.createConfirmGroup(request)
    return redirect('/')

@csrf_exempt
def groupsPostMessage(request):
    if request.session.get('username', False):
        controller = gController()
        return controller.postMessageGroup(request)
    return redirect('/')

@csrf_exempt
def groupsGetChat(request, id):
    if request.session.get('username', False):
        controller = gController()
        return controller.getChatGroup(request, id)
    return redirect('/')

@csrf_exempt
def tutorsUsersEdit(request,id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersEdit(request, id)
    return redirect('/')

@csrf_exempt
def tutorsUsersDelete(request):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersDelete(request)
    return redirect('/')

@csrf_exempt
def tutorsUsersDeleteById(request, id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersDeleteById(request, id)
    return redirect('/')

@csrf_exempt
def tutorsUsersAdd(request):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersAdd(request)
    return redirect('/')

@csrf_exempt
def tutorsUsersAddConfirm(request):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersAddConfirm(request)
    return redirect('/')

@csrf_exempt
def tutorsEditUsersPictograms(request):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsEditUsersPictograms(request)
    return redirect('/')

@csrf_exempt
def tutorsEditUserPassword(request, id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsEditUserPassword(request, id)
    return redirect('/')

@csrf_exempt
def groupsCreate(request):
    if request.session.get('username', False):
        if request.method == 'GET':
            controller = gController()
            return controller.createGroup(request)
    return redirect('/')
@csrf_exempt
def tutorsTasks(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            controller = Controller()
            return controller.tutorTasks(request)
    return redirect('/')

@csrf_exempt
def tutorsTasksDetail(request, id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorTasksDetail(request, id)
    return redirect('/')


@csrf_exempt
def tutorsTasksDelete(request, id):
    if request.method == 'GET':
        if request.session.get('username', False):
            controller = Controller()
            return controller.tutorTasksDelete(request, id)
    return redirect('/')

@csrf_exempt
def tutorTasksCreate(request):
    if request.method == 'POST':
        if request.session.get('username', False):
            controller = Controller()
            return controller.tutorTasksCreate(request)
    return redirect('/')


@csrf_exempt
def tasksChat(request, identifier):
    if request.session.get('username', False):
        controller = Controller()
        if request.method == 'GET':
            return controller.chatTask(request, identifier)
        elif request.method == 'POST':
            return controller.postChatTask(request, identifier)
    return redirect('/')

@csrf_exempt
def deviceToken(request):
    if request.method == 'POST':
        controller = Controller()
        return controller.deviceToken(request)
      