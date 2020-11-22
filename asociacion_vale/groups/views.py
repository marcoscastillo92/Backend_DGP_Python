from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Groups
from groups.controller import  Controller

import json

# Create your views here.
@csrf_exempt
def index(request):
    pass

@csrf_exempt
def groupsCreate(request):
    if request.method == 'POST':
        controller = Controller()
        return controller.createGroup(request)

@csrf_exempt
def groupsGet(request):
    if request.method == 'GET':
        controller = Controller()
        return controller.getGroups(request)
    
    

