import json

from django.http import JsonResponse
from django.shortcuts import HttpResponse

from users.models import User
from .models import Rating, Task, Progress, Category, TaskStatus


def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value


def getUserByToken(token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

def createTask(request):
    task = Task(request.body)
    task.save()
    return JsonResponse(task.serializeCustom)

def assignTask(request):
    #TODO
    if request.method == 'POST':
        task = Task.objects.get(id=request.body.taskId)
        user = User.objects.get(id=request.body.userId)
        userProgress = Progress.objects.all(user=user, category = task.category)
        progress = Progress(user=user, category = task.category, total=userProgress.lenght+1)

def rateTask(request):
    token = request.META['HTTP_AUTHORIZATION']
    author = getUserByToken(token)
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
    author = getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)

    task = Task.objects.get(id=id)
    response = {}
    append_value(response, 'task', task.serializeCustom(token))
    return JsonResponse(response)

def getAllTasks(request):
    token = request.META['HTTP_AUTHORIZATION']
    author = getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)

    tasks = Task.objects.filter(users__id=User.objects.get(token=token).id)
    response = {}
    for task in tasks:
        append_value(response, 'tasks', task.serializeCustom(token))
    return JsonResponse(response)

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

def getTaskStatus(request):
    token = request.META['HTTP_AUTHORIZATION']
    requestData = json.loads(request.body)
    author = getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)
    task = Task.objects.get(id=requestData.get('id'))
    if task:
        taskStatus = TaskStatus.objects.get(user=author, task=task)
        if taskStatus:
            return JsonResponse({"status":taskStatus.serializeCustom()}, safe=False)
        return JsonResponse({"result":"error", "message":"No hay estado para la tarea"}, safe=False)
    return JsonResponse({"result":"error", "message":"No existe la tarea"}, safe=False)

def setTaskStatus(request):
    token = request.META['HTTP_AUTHORIZATION']
    requestData = json.loads(request.body)
    author = getUserByToken(token)
    if not author:
        response = {"result":"error", "message":"El usuario no existe"}
        return JsonResponse(response, safe=False)
    task = Task.objects.get(id=requestData.get('idTask'))
    user = User.objects.get(id=requestData.get('idUser'))
    if task:
        taskStatus = TaskStatus.objects.get(user=user, task=task)
        if taskStatus:
            alreadyDone = taskStatus.done
            substract = False
            if taskStatus.done and not requestData.get('done'):
                substract = True
            taskStatus.done = bool(requestData.get('done'))
            taskStatus.save(force_update=True)
            progress = Progress.objects.get(user=user, category=task.category)
            if progress:
                if bool(requestData.get('done')) and not alreadyDone:
                    progress.done = progress.done + 1
                elif substract:
                    progress.done = progress.done - 1
                progress.save(force_update=True)
            return JsonResponse({"status":taskStatus.serializeCustom()}, safe=False)
        return JsonResponse({"result":"error", "message":"No hay estado para la tarea"}, safe=False)
    return JsonResponse({"result":"error", "message":"No existe la tarea"}, safe=False)