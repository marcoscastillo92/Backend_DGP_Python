from django.shortcuts import redirect, render
from users.models import User
from forums.models import Forum
from tasks.models import Task, TaskStatus, Rating
from tasks import forms
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.contrib.auth.hashers import check_password
import json


def handle_upload_image_task_form(f):
    fileName = 'static/uploads/'+f.name
    with open(fileName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fileName


class Controller:
    def getUserByToken(self, token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

    def getMessages(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        userFromDB = self.getUserByToken(token)
        if userFromDB:
            identifier = request.GET.get('identifier')
            category = request.GET.get('category')
            if category == 'task':
                lista = Forum.objects.filter(identifier=identifier, emisorUser=userFromDB) | Forum.objects.filter(
                    identifier=identifier, receptorUser=userFromDB)
            elif category == 'group':
                lista = Forum.objects.filter(identifier=identifier)
            myList = list(lista.order_by('createdAt').reverse())

            var = []
            for l in myList:
                print(l.id)
                if l.emisorUser_id:
                    user = User.objects.filter(id=l.emisorUser_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor_name": user[0].name, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path, "tutor": False}
                    var.append(respuesta)

                if l.emisorTutor_id:
                    user = Tutor.objects.filter(id=l.emisorTutor_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor_name": user[0].name, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path, "tutor": True}
                    var.append(respuesta)
            print(var)
            formatResponse = {"mensajes": var}
            return JsonResponse(formatResponse, safe=False)
        else:
            response = {"result": "error", "message": "El usuario no existe"}
            return JsonResponse(response, safe=False)

    def getMessagesTutors(self, request):
        identifier = request.GET.get('identifier')
        lista = Forum.objects.filter(identifier=identifier)
        myList = list(lista.order_by('createdAt'))

        var = []
        for l in myList:
            if l.emisorUser_id:
                user = User.objects.filter(id=l.emisorUser_id)
                print(user[0].username)
                respuesta = {"body": l.body, "emisor": user[0].username, "created": l.createdAt,
                             "identifier": l.identifier, "mimeType": l.mimeType.path}
                var.append(respuesta)

            if l.emisorTutor_id:
                user = Tutor.objects.filter(id=l.emisorTutor_id)
                print(user[0].username)
                respuesta = {"body": l.body, "emisor": user[0].username, "created": l.createdAt,
                             "identifier": l.identifier, "mimeType": l.mimeType.path}
                var.append(respuesta)
        formatResponse = {"mensajes": var}
        return formatResponse

    def postMessage(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        userFromDB = self.getUserByToken(token)
        if userFromDB:
            bodyData = json.loads(request.body)
            # {idForum:int,messageType: "string",body:"string", mimeType}
            identifier = bodyData['identifier']
            forum = Forum.objects.filter(identifier=identifier, category="welcomeMessage")  # mensaje creado por defecto
            if forum:
                body = bodyData['body']
                mimeType = bodyData['mimeType']
                category = bodyData['category']
                newForum = Forum(
                    body=body,
                    emisorTutor=None,
                    emisorUser=userFromDB,
                    receptorTutor=forum[0].emisorTutor,  # obtener el tutor en la sesión,
                    receptorUser=None,
                    mimeType=mimeType,
                    category=category,
                    identifier=identifier
                )
                newForum.save()
                response = {"result": "success", "message": "El mensaje se ha almacenado correctamente"}
                return JsonResponse(response, safe=False)
            else:
                response = {"result": "error", "message": "El foro no existe"}
                return JsonResponse(response, safe=False)
            messagesForum = list(Forum.objects.filter(id=idForum).values())
            return JsonResponse(messagesForum, safe=False)
        else:
            response = {"result": "error", "message": "El usuario no existe"}
            return JsonResponse(response, safe=False)

    def tutorLogin(self, request):
        print(request.POST)
        if not request.POST.get('username', False) or not request.POST.get('password', False):
            context = {'msg': '*Todos los campos son obligatorios'}
            return render(request, './tutors/index.html', context)
        else:
            tutorPass = Tutor.objects.filter(username=request.POST.get('username')).values('password')
            userID = Tutor.objects.filter(username=request.POST.get('username')).values('id')
            if tutorPass:
                if check_password(request.POST.get('password'), tutorPass[0]['password']):
                    request.session['username'] = request.POST.get('username')
                    return redirect('/tutors/home')
                else:
                    context = {'msg': '*Contraseña incorrecta'}
                    return render(request, './tutors/index.html', context)
            else:
                context = {'msg': '*El usuario no existe'}
                return render(request, './tutors/index.html', context)

    def tutorGroups(self, request):

        return render(request, './tutors/groups.html')

    def tutorTasks(self, request):
        tutor = Tutor.objects.filter(username=request.session.get('username'))[0]
        taskStatus = TaskStatus.objects.filter(tutor=tutor)
        tasks = []
        for status in taskStatus:
            if not status.task in tasks:
                tasks.append(status.task)
        taskForm = forms.TaskForm(request.POST or None, request.FILES or None)
        taskForm.fields['image'].required = False
        taskForm.fields['media'].required = False
        context = {'tutor': tutor, 'tasks': tasks, 'form': taskForm}
        return render(request, './tutors/tasks.html', context)

    def tutorTasksDetail(self, request, id):
        infoTask = Task.objects.get(id=id)
        tutor = Tutor.objects.get(username=request.session.get('username'))
        taskStatus = {}
        ratings = {}
        count = 0
        for user in infoTask.users.all():
            status = TaskStatus.objects.get(user=user, task=infoTask, tutor=tutor)
            if status:
                valueStatus = {'status': status, 'user': user}
                if count in taskStatus:
                    taskStatus[count].append(valueStatus)
                else:
                    taskStatus[count] = valueStatus
            try:
                rating = Rating.objects.get(user=user, task=infoTask)
            except:
                rating = None
            if rating:
                valueRating = {'user': user.username, 'rating': rating}
                if count in taskStatus:
                    ratings[count].append(valueRating)
                else:
                    ratings[count] = valueRating
            count = count + 1

        taskForm = forms.TaskForm(request.POST or None, request.FILES or None, instance=infoTask)
        taskForm.fields['image'].required = False
        taskForm.fields['media'].required = False
        context = {'task': infoTask, 'form': taskForm, 'taskStatus': taskStatus, 'ratings': ratings}
        if request.method == 'POST':
            # Guardar cambios
            if taskForm.is_valid():
                taskForm.save()
                return render(request, 'tutors/task-detail.html', context)
        return render(request, 'tutors/task-detail.html', context)

    def tutorTasksDelete(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('tutorTasks')

    def tutorTasksCreate(self, request):
        taskForm = forms.TaskForm(request.POST or None, request.FILES or None)
        taskForm.fields['image'].required = False
        taskForm.fields['media'].required = False
        taskForm.save()
        return redirect('tutorTasks')
        pass

    def chatTask(self, request, identifier):
        context = {}
        messages = self.getMessagesTutors(request)
        if identifier:
            taskFromDB = Task.objects.filter(identifier=identifier)
            context['task'] = taskFromDB[0]
        if messages:
            context['messages'] = messages
        context['tutor'] = request.session.get('username')
        return render(request, './tutors/task-chat.html', context)

    def postChatTask(self, request, identifier):
        message = Forum(body=request.POST.get('text'), )
        return redirect('taskChat', identifier=identifier)
