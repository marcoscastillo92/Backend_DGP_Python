from .models import Rating, Task, Progress, Category
from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponseNotAllowed
from users.models import User
import json

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
    task = Task.objects.get(id=id)
    response = json.dumps(task.serializeCustom(token))
    return HttpResponse(response, content_type="text/json-comment-filtered")

def getAllTasks(request):
    token = request.META['HTTP_AUTHORIZATION']
    tasks = Task.objects.filter(users__id=User.objects.get(token=token).id)
    response = "{"
    for task in tasks:
        response += json.dumps(task.serializeCustom(token)) + ","
    response += "}"
    return HttpResponse(response, content_type="text/json-comment-filtered")

def saveRandomTask(request):
    category = Category(title='Categoría random')
    category.save()
    newTask = Task(
        title = 'Random Task',
        shortDescription = 'Tarea de prueba aleatoria, esto es la descripción corta',
        fullDescription = 'Esto es la descripción larga de la tarea aleatoria para pruebas, ',
        category = category
    )
    newTask.save()
    category2 = Category(title='Categoría random 2')
    category2.save()
    newTask2 = Task(
        title = 'Random Task 2',
        shortDescription = 'Tarea de prueba aleatoria, esto es la descripción corta',
        fullDescription = 'Esto es la descripción larga de la tarea aleatoria para pruebas, ',
        category = category2
    )
    newTask2.save()
    newTask3 = Task(
        title = 'Random Task 2',
        shortDescription = 'Tarea de prueba aleatoria, esto es la descripción corta',
        fullDescription = 'Esto es la descripción larga de la tarea aleatoria para pruebas, ',
        category = category2
    )
    newTask3.save()
    response = json.loads('{"result": "success", "message": "Tarea creada correctamente"}')
    return JsonResponse(response)

def getRandomTask(request):
    randomTask = list(Task.objects.filter(title__contains='Random Task').values())
    if randomTask:
        response = {"task": randomTask}
    return JsonResponse(response, safe=False)