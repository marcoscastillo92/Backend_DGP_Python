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
            return gControler.saveMessage(requestData)
        if requestData['messageType'] == 'forumUser':
            return uControler.saveMessage(requestData)
        #if requestData['messageType'] == 'forumTask':
            #controller.saveMessage(request)
        