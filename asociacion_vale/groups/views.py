from django.shortcuts import render
from .models import Groups
from json import json

# Create your views here.
def groupsCreate(request):
    if request.method == 'POST':
        bodyUnicode = request.body.decode('utf-8')
        userData = json.loads(bodyUnicode)
        group = Groups(
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
        group.save()
    return JsonResponse(json.loads('{"name":"Marcos", "apellidos":"Castillo Trigueros"}'))