from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from users.models import User
from users.controller import Controller

NEEDED_USERS_FIELDS =  ["name","username","password","role"]
ALL_USERS_FIELDS =  ["name","username","password","role","email","phoneNumber","birthDay"]
NEEDED_USER_LOGIN_FIELDS = ["password"]
ALL_USER_LOGIN_FIELDS = ["password"]
# Create your views here.
def index(request):
    return HttpResponse("API para la Asociación Vale.")

def correctFields(request,neededFields, allFields ):
    missingFields = []
    extraFields = []

    return
    
@csrf_exempt
def users_create(request):
    if request.method == 'POST':
        bodyUnicode = request.body.decode('utf-8')
        print(bodyUnicode)
        userData = json.loads(bodyUnicode)
        print(userData)
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



def user_login(request):

    return

def users_login(request):
    if request.method == 'POST':
        if request.session and request.session.user:
            response = json.dumps({"result": "error", "message" : "You are already logged"})
            return response

    return user_login(request)
    