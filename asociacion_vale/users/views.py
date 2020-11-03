from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
import json
from .models import User
from .controller import Controller

# Create your views here.
def index(request):
    return HttpResponse("API para la Asociación Vale.")

def correctFields(request,neededFields, allFields ):
    missingFields = []
    extraFields = []

    return
    
@csrf_exempt
def usersCreate(request):
    if request.method == 'POST':
        bodyUnicode = request.body.decode('utf-8')
        userData = json.loads(bodyUnicode)
        user = User(
            name= userData["name"],
            email= userData["email"],
            username= userData["username"],
            password= userData["password"],
            phoneNumber= userData["phoneNumber"],
            profileImage= userData ["profileImage"],
           # role= userData ["role"],
           # birthDate= userData["birthDate"],
            #gender= userData["gender"]
        )
        user.save()
    return JsonResponse(json.loads('{"name":"Marcos", "apellidos":"Castillo Trigueros"}'))

@csrf_exempt
def usersLogin(request):
    controller = Controller()
    if request.method == 'POST':
        return controller.usersLogin(request)
        
    
@csrf_exempt
def pictograms(request):
    controller = Controller()
    if request.method == 'GET':
        return controller.getPictograms(request)
    if request.method == 'POST':
        return controller.savePictograms(request)
        

@csrf_exempt
def randomUser(request):
    controller = Controller()
    if request.method == 'GET':
        return controller.getRandomUser(request)
    if request.method == 'POST':
        return controller.saveRandomUser(request)
        


