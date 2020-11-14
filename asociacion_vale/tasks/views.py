from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Rating, Task
import tasks.controller as TaskController
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
    return HttpResponseBadRequest("BAD REQUEST")

@csrf_exempt
def createTask(request):
    if request.method == 'POST':
        return TaskController.createTask(request)
    return HttpResponseBadRequest("BAD REQUEST")

@csrf_exempt
def deleteTask(request, id):
    if request.method == 'DELETE':
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponse("Deleted")
    return HttpResponseBadRequest("BAD REQUEST")

@csrf_exempt
def getTask(request, id):
    if request.method == 'GET':
        return TaskController.getTask(request, id)
    return HttpResponseBadRequest("BAD REQUEST")

@csrf_exempt
def getAllTasks(request):
    if request.method == 'GET':
        return TaskController.getAllTasks(request)
    return HttpResponseBadRequest("BAD REQUEST")

@csrf_exempt
def rateTask(request):
    if request.method == 'POST':
        return TaskController.rateTask(request)
    return HttpResponseBadRequest("BAD REQUEST")