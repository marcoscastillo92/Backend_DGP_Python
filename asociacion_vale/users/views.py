from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
import json
from .models import User
from .controller import Controller
import secrets

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
        
#Metodo para generar una contraseña
@csrf_exempt
def generatePassword(request):
    if request.method == 'GET':
        controller = Controller()
        d = controller.generatePassword(request)
        possibleKeys = []
        possibleNames = []

        for x in d:
            array = json.loads(x)
            for index in range(len(array)):
                possibleKeys.append(array[index]["key"])
                possibleNames.append(array[index]["name"])
            
        password = ""
        secret = 0
        names = ""
        for i in range(len(possibleKeys)):
           secret = secrets.randbelow(len(possibleKeys))
           password +=  possibleKeys[secret] #Se obtiene una key aleatoria
           names += " " + possibleNames[secret]
        
        response =json.dumps({"names" : names,"password" : password}, separators=(',', ':'))
        return JsonResponse(response , safe=False)
         