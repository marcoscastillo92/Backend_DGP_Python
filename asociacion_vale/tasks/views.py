from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Task
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

def getTask(request):
    if request.method == 'GET':
        task = Task.objects.get(id=request.query.id_tarea)
        return task
    return None

def getAllTasks(request):
    if request.method == 'GET':
        user = User.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        tasks = Task.objects.all(user=user)