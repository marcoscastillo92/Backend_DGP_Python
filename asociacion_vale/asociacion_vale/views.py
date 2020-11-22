from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .controller import Controller
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
    if request.method == 'GET':
        # Borro la cookie de usurname que es la que me dice si estoy logueado
        del request.session['username']
        request.session.modified = True
        return redirect('/')


@csrf_exempt
def tutorsGroup(request):
    if request.method == 'GET':
        controller = Controller()
        return controller.tutorGroups(request)


@csrf_exempt
def tutorsTasks(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            controller = Controller()
            return controller.tutorTasks(request)
    return redirect('/')

@csrf_exempt
def tutorsTasksEdit(request, id):
    if request.session.get('username', False):
        controller = Controller()
        return controller.tutorTasksEdit(request, id)
    return redirect('/')


@csrf_exempt
def tutorsTasksDelete(request, id):
    if request.method == 'GET':
        if request.session.get('username', False):
            controller = Controller()
            return controller.tutorTasksDelete(request, id)
    return redirect('/')
