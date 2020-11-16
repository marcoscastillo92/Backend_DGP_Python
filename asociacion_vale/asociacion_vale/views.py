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
        