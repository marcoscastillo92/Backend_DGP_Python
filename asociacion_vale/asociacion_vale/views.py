from django.http.response import HttpResponse
from django.shortcuts import render
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
        
        return render(request,'./tutors/index.html')


@csrf_exempt
def tutorsLogin(request):
    if request.method == 'POST':
        controller = Controller()
        return controller.tutorLogin(request)
        

@csrf_exempt
def tutorsHome(request):
    if request.method == 'GET':
        
        return render(request,'./tutors/home.html')
        