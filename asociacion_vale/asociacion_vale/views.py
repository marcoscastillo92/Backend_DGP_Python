from django.shortcuts import render
from users.controller import Controller as userController
from groups.controller import Controller as groupController
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def postMessage(request):
    if request.method == 'POST':
        bodyUnicode = request.body.decode('utf-8')
        requestData = json.loads(bodyUnicode)
        gControler = groupController()
        uControler = userController()

        #Publicar un mensaje tipo forum
        if requestData['messageType'] == 'forumGroup':
            return gControler.saveMessage(request)
        if requestData['messageType'] == 'forumUser':
            return uControler.saveMessage(request)
#        if requestData['messageType'] == 'forumTask':
#            return tController.saveMessage(request)


@csrf_exempt
def getMessages(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        requestData = json.loads(body_unicode)
        
        gControler = groupController()
        uControler = userController()

        #Publicar un mensaje tipo forum
        if requestData['messageType'] == 'forumGroup':
            return gControler.getMessages(request)
        if requestData['messageType'] == 'forumUser':
            return uControler.getMessages(request)
        #if requestData['messageType'] == 'forumTask':
            #controller.getMessages(request)
        