from .models import Rating, Task, Progress
from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseNotAllowed
from users.models import User
from forums.models import Forum
from django.contrib.auth.models import User as Tutor
import json

def getUserByToken(self, token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

def messageManagement(request):
    bodyUnicode = request.body.decode('utf-8')
    requestData = json.loads(bodyUnicode)

    #Publicar un mensaje tipo forum
    if requestData['messageType'] == 'forum':
        print() 
    pass

def createTask(request):
    task = Task(request.body)
    task.save()
    return JsonResponse(json.loads(task.serializeCustom))

def assignTask(request):
    if request.method == 'POST':
        task = Task.objects.get(id=request.body.taskId)
        user = User.objects.get(id=request.body.userId)
        userProgress = Progress.objects.all(user=user, category = task.category)
        progress = Progress(user=user, category = task.category, total=userProgress.lenght+1)

def rateTask(request):
    token = request.META['HTTP_AUTHORIZATION']
    author = self.getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)

    bodyData = json.loads(request.body)
    idTask = bodyData['id_tarea']
    newRating = False
    try:
        rating = Rating.objects.get(task__id=idTask, user__token=token)
    except:
        newRating = True

    if not newRating:
        text = bodyData['text'] if bodyData['text'] else rating.text 
        difficulty = bodyData['dificultad'] if bodyData['dificultad'] else rating.difficulty 
        utility = bodyData['utilidad'] if bodyData['utilidad'] else rating.utility 
        rating.text = text
        rating.difficulty = difficulty
        rating.utility = utility
        rating.save()
    else:
        rating = Rating(task=Task.objects.get(id=idTask),user=User.objects.get(token=token),text=bodyData['text'],utility=bodyData['utilidad'],difficulty=bodyData['dificultad'])
        rating.save()
    return JsonResponse(json.loads('{"status":"success", "message":"mensaje valorado correctamente"}'))

def getTask(request, id):
    token = request.META['HTTP_AUTHORIZATION']
    author = self.getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)

    task = Task.objects.get(id=id)
    response = json.dumps(task.serializeCustom(token))
    return HttpResponse(response, content_type="text/json-comment-filtered")

def getAllTasks(request):
    token = request.META['HTTP_AUTHORIZATION']
    author = self.getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)

    tasks = Task.objects.filter(users__id=User.objects.get(token=token).id)
    response = "{"
    for task in tasks:
        response += json.dumps(task.serializeCustom(token)) + ","
    response += "}"
    return HttpResponse(response, content_type="text/json-comment-filtered")