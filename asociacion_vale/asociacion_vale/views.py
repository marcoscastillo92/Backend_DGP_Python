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
    if request.method == 'GET':
        
        return render(request,'./tutors/index.html')


@csrf_exempt
def tutorsLogin(request):
    if request.method == 'POST':
        controller = Controller()
        return controller.tutorLogin(request)
        

@csrf_exempt
def tutorsHome(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            return render(request,'./tutors/home.html')
        else:
            return redirect('/')
@csrf_exempt
def tutorsLogout(request):
    if request.method == 'GET':
        #Borro la cookie de usurname que es la que me dice si estoy logueado
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
def groupsEdit(request):
    if request.session.get('username', False):
        if request.method == 'GET':
            controller = gController()
            return controller.editGroup(request)
    return redirect('/')
@csrf_exempt
def groupsEditConfirm(request):
    if request.session.get('username', False):
        if request.method == 'POST':
            controller = gController()
            return controller.editConfirmGroup(request)
    return redirect('/')
@csrf_exempt
def groupsChat(request):
    if request.session.get('username', False):
        if request.method == 'GET':
            controller = gController()
            return controller.chatGroup(request)

    return redirect('/')
@csrf_exempt
def tutorsUsersEdit(request,id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorsUsersEdit(request, id)
    return redirect('/')