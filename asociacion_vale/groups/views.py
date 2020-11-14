from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Groups
from .models import ForumGroup
import json

# Create your views here.
@csrf_exempt
def index(request):
    pass

@csrf_exempt
def groupsCreate(request):
    if request.method == 'POST':
        groupData = json.loads(request.body)
        group = Groups(
            name= groupData['name'],
        )
        group.save()
       
        string = '{"Name":"'+groupData['name']+' "}"'
    return JsonResponse(json.loads(string))

@csrf_exempt
def groupsGet(request, id):
    pass


