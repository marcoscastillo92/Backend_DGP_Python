from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from users.models import User

# Create your views here.
def index(request):
    return HttpResponse("API para la Asociación Vale.")

def users_create(request):
    if request.method == 'POST':
        bodyUnicode = request.body.decode('uft-8')
        userData = json.loads(bodyUnicode)
        user = User(
            name= userData.name,
            email= userData.email,
            username= userData.username,
            password= userData.password,
            phoneNumber= userData.phoneNumber,
            profileImage= userData.profileImage,
            role= userData.role,
            birthDate= userData.birthDate,
            gender= userData.gender
        )
        user.save()
    return JsonResponse(json.loads('{"name":"Marcos", "apellidos":"Castillo Trigueros"}'))