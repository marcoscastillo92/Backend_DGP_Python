from django.shortcuts import redirect, render
from users.models import User
from forums.models import Forum
from tasks.models import Task, TaskStatus
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.contrib.auth.hashers import check_password
import json


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
            bodyData = json.loads(request.body)
            identifier = bodyData['identifier']
            category = bodyData['category']
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
                    respuesta = {"body": l.body, "emisor": user[0].username, "created": l.createdAt,
                                 "identifier": l.identifier, "mimeType": l.mimeType.path}
                    var.append(respuesta)

                if l.emisorTutor_id:
                    user = Tutor.objects.filter(id=l.emisorTutor_id)
                    print(user[0].username)
                    respuesta = {"body": l.body, "emisor": user[0].username, "created": l.createdAt,
                                 "identifier": l.identifier, "mimeType": l.mimeType.path}
                    var.append(respuesta)
            print(var)
            formatResponse = {"mensajes": var}
            return JsonResponse(formatResponse, safe=False)
        else:
            response = {"result": "error", "message": "El usuario no existe"}
            return JsonResponse(response, safe=False)

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
        context = {'tutor': tutor, 'tasks': tasks}
        #print(tasks[0].serializeCustom("dbbdbd"))
        return render(request, './tutors/tasks.html', context)
