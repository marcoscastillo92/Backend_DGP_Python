from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Rating, Task
from .controller import Controller as TaskController
from users.models import User
import json

@csrf_exempt
def categoryCreate(request):
    if request.method == 'POST':
        categoryData = json.loads(request.body)
        group = Category(
            name= categoryData['name']
        )
        group.save()
        string = '{"Name":"'+categoryData['name']+'"}'
    return JsonResponse(json.loads(string))

@csrf_exempt
def createTask(request):
    return TaskController.createTask

@csrf_exempt
def getTask(request, id):
    if request.method == 'GET':
        token = request.META['HTTP_AUTHORIZATION']
        task = Task.objects.get(id=id)
        return HttpResponse(json.dumps(task.serializeCustom(token)), content_type="text/json-comment-filtered")
    return HttpResponse("OK")

@csrf_exempt
def getAllTasks(request):
    if request.method == 'GET':
        token = request.META['HTTP_AUTHORIZATION']
        tasks = Task.objects.filter(users__id=User.objects.get(token=token).id)
        response = "{"
        for task in tasks:
            response += json.dumps(task.serializeCustom(token)) + ","
        response += "}"
        print(response)
        return HttpResponse(response, content_type="text/json-comment-filtered")

@csrf_exempt
def rateTask(request):
    if request.method == 'POST':
        token = request.META['HTTP_AUTHORIZATION']
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
    return HttpResponse("BAD")