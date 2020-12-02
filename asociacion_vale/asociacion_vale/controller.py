from django.shortcuts import redirect, render
from users.models import User, Pictograms
from forums.models import Forum
from groups.models import Groups
from tasks.models import Task, TaskStatus, Rating, Category
from tasks import forms
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.contrib.auth.hashers import check_password
import json
from users import forms as uForm
from users.controller import Controller as uController



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

    def getMessagesTutors(self, id):
            lista = Forum.objects.filter(identifier=id)
            myList = list(lista.order_by('createdAt'))

            var = []
            for l in myList:
                if l.emisorUser_id:
                    user = User.objects.filter(id = l.emisorUser_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path}
                    var.append(respuesta)

                if l.emisorTutor_id:
                    user = Tutor.objects.filter(id = l.emisorTutor_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path}
                    var.append(respuesta)
            formatResponse = {"mensajes" : var}
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

    def postMessageTutor(self, request):
        identifier = request.POST.get('identifier')
        forum = Forum.objects.filter(identifier = identifier, category="welcomeMessage") #mensaje creado por defecto
        if forum:
            body = request.POST.get('body')
            mimeType = request.POST.get('mimeType')
            category = request.POST.get('category')
            newForum = Forum(
                body = body,
                emisorTutor = forum[0].emisorTutor,
                emisorUser = None,
                receptorTutor = None,
                receptorUser = None,
                mimeType = mimeType,
                category = category,
                identifier = identifier
            )
            newForum.save()
            return True
        else:
            return False

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

    def tutorGroups(self,request):
        context = {}
        listGroups = list(Groups.objects.filter(tutors__username = request.session.get('username')).order_by('createdAt').reverse().values())
        listUsers = list(User.objects.all().values())

        if listUsers:
            arrayUsers = []
            for user in listUsers:
                arrayUsers.append(user)
            context['users'] = arrayUsers
        if listGroups:
            arrayGroups = []
            for group in listGroups:
                arrayGroups.append(group)
            context['groups'] = arrayGroups

        return render(request,'./tutors/groups.html', context)

    def tutorUsers(self,request):
        context = {}
        listUsers = list(User.objects.all().order_by('name').values())

        if listUsers:
            arrayUsers = []
            for user in listUsers:
                arrayUsers.append(user)
            context['users'] = arrayUsers
        return render(request,'./tutors/users.html', context)


    def tutorsUsersEdit(self,request,id):
        infoUser = User.objects.get(id=id)
        userForm = uForm.UserForm(request.POST or None, request.FILES or None, instance=infoUser)
        userForm.fields['profileImage'].required = False
        #userForm.fields['media'].required = False
        context = {'task': infoUser, 'form': userForm , 'id' : id}
        if request.method == 'POST':
            # Guardar cambios
            if userForm.is_valid():
                userForm.save()
                context['response']='success'
                return render(request, 'tutors/editUser.html', context)
        return render(request, 'tutors/editUser.html', context)

    def tutorsUsersAdd(self, request):
        userForm = uForm.UserForm(request.POST or None, request.FILES or None)
        #userForm.fields['media'].required = False
        context = {'form': userForm}
        if request.method == 'GET':
            # Guardar cambios
            return render(request, 'tutors/addUser.html', context)
        if request.method == 'POST':
            # Guardar cambios
            if userForm.is_valid():
                userForm.save()
                return render(request, 'tutors/addUser.html', context)

    def tutorsUsersAddConfirm(self, request):
        userForm = uForm.UserForm(request.POST or None, request.FILES or None)
        #userForm.fields['media'].required = False
        if request.method == 'POST':
            # Guardar cambios
            if userForm.is_valid():
                userForm.save()
                userFromDB = User.objects.filter(username=request.POST.get('username'))
                pictogramsFromDB= list(Pictograms.objects.all().values())
                if not pictogramsFromDB:
                    userControler = uController()
                    userControler.savePictograms(request)
                    pictogramsFromDB= list(Pictograms.objects.all().values())
                context = {'form': userForm, 'params':request.POST, 'id':userFromDB[0].id, 'pictograms': pictogramsFromDB}
                return render(request, 'tutors/addUserPictograms.html', context)

    def tutorsUsersDelete(self, request):
        if request.method == 'POST':
            userFromDB = User.objects.filter(id=request.POST.get('id'))
            if userFromDB:
                userFromDB.delete()
                return redirect('/tutors/users')

    def tutorsUsersDeleteById(self, request, id):
        if request.method == 'GET':
            userFromDB = User.objects.filter(id=id)
            if userFromDB:
                userFromDB.delete()
                return redirect('/tutors/users')

    def tutorsEditUsersPictograms(self, request):
        if request.method == 'POST':
            pictogramSize = 6
            userId = request.POST.get('id')
            firstPictogram = request.POST.get('firstPictogram')
            secondPictogram = request.POST.get('secondPictogram')
            thirdPictogram = request.POST.get('thirdPictogram')
            fourthPictogram = request.POST.get('fourthPictogram')
            fifthPictogram = request.POST.get('fifthPictogram')
            sixthPictogram = request.POST.get('sixthPictogram')

            arrayPictograms = [firstPictogram, secondPictogram, thirdPictogram, fourthPictogram, fifthPictogram, sixthPictogram]
            listPictograms = list(Pictograms.objects.all().values())
            password = ""
            for index in range(0, pictogramSize):
                for pictogram in listPictograms:
                    if pictogram['name'] == arrayPictograms[index]:
                        password += pictogram['key']
            userFromDB = User.objects.get(id=userId)
            userFromDB.password = password
            userFromDB.save()
            return redirect('/tutors/users')


    def tutorsEditUserPassword(self, request, id):
        if request.method == 'GET':
            pictogramsSize = 6
            pictogramsFromDB= list(Pictograms.objects.all().values())
            userFromDB = User.objects.filter(id=id)
            userPassword = userFromDB[0].password
            userPictogramConfig = []
            passwordSize = len(userFromDB[0].password)
            indexSubstring = passwordSize // pictogramsSize
            print(userPassword)
            for i in range(0, pictogramsSize):
                substring = userPassword[indexSubstring * i: ((i+1)*indexSubstring)]
                print(substring)
                for pictogram in pictogramsFromDB:
                    if substring == pictogram['key']:
                        userPictogramConfig.append(pictogram['name'])
            print(userPictogramConfig)

            context = {'id':id, 'pictograms': pictogramsFromDB, 'userPictograms': userPictogramConfig}
            return render(request, 'tutors/addUserPictograms.html', context)


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
        users = User.objects.all()
        context = {'tutor': tutor, 'tasks': tasks, 'form': taskForm, 'users': users}
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
        categoryForm = forms.CategoryForm()
        allUsers = list(User.objects.all().values())
        usersOut = []
        usersIn = []

        for i in allUsers:
            usersOut.append(i)

        if request.method == 'GET':
            for i in infoTask.users.all():
                usersIn.append(i)

        if request.method == 'POST':
            # Guardar cambios
            if taskForm.is_valid():
                taskForm.save()
                usersInTask = request.POST.getlist('listUsers')
                for i in usersInTask:
                    userToAdd = User.objects.get(id=int(i))
                    if userToAdd not in usersIn:
                        usersIn.append(userToAdd)

        for i in range(len(usersOut)):
            for j in usersIn:
                if usersOut[i].get('username') == j.username:
                    usersOut.pop(i)
            break

        if request.method == 'POST':
            if taskForm.is_valid():
                for user in usersIn:
                    if user not in taskForm.instance.users.all():
                        taskForm.instance.users.add(user)
                for user in usersOut:
                    if user in taskForm.instance.users.all():
                        taskForm.instance.users.remove(user)
        context = {'task': infoTask, 'form': taskForm, 'taskStatus': taskStatus, 'ratings': ratings,
                   'categoryForm': categoryForm, 'users': usersOut, 'usersIn': usersIn}
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
        usersInTask = request.POST.getlist('listUsers')
        for user in usersInTask:
            userFromDB = User.objects.get(id=int(user))
            if userFromDB:
                taskForm.instance.users.add(userFromDB)
        taskForm.instance.save()
        return redirect('tutorTasksEdit', id=taskForm.instance.id)
        pass

    def chatTask(self, request, identifier, userId):
        context = {}
        lista = Forum.objects.filter(identifier=identifier).values()
        messagesTask = list(lista.order_by('createdAt'))
        tutor = Tutor.objects.get(username=request.session.get('username'))
        context['userId'] = userId
        user = User.objects.get(id=userId)
        messages = []
        for message in messagesTask:
            if message.get('emisorUser_id') == userId:
                messages.append({"body": message.get('body'), "emisor": user.username, "created": message.get('createdAt'), "identifier": message.get('identifier'), "mimeType": message.get('mimeType')})
            elif message.get('emisorTutor_id') == tutor.id:
                messages.append({"body": message.get('body'), "emisor": tutor.username, "created": message.get('createdAt'), "identifier": message.get('identifier'), "mimeType": message.get('mimeType')})

        if identifier:
            taskFromDB = Task.objects.filter(identifier=identifier)
            context['task'] = taskFromDB[0]
        if messages:
            context['messages'] = messages
        context['tutor'] = request.session.get('username')
        return render(request, './tutors/task-chat.html', context)

    def postChatTask(self, request, identifier, userId):
        tutor = Tutor.objects.get(username=request.session.get('username', False))
        user = User.objects.get(id=userId)
        body = request.POST.get('body')
        mimeType = request.FILES.get('mimeType')
        category = request.POST.get('category')
        newForum = Forum(
            body=body,
            emisorTutor=tutor,
            emisorUser=None,
            receptorTutor=None,
            receptorUser=user,
            mimeType=mimeType,
            category=category,
            identifier=identifier
        )
        newForum.save()
        return redirect('taskChat', identifier=identifier, userId=userId)

    def createCategory(self, request):
        idTask = request.POST.get('taskId')
        category = forms.CategoryForm(request.POST)
        category.save()
        return redirect('tutorTasksEdit', id=idTask)
    #
    # def tutorTasksCreate2(self, request):
    #     title = request.POST.get('title')
    #     shortDescription = request.POST.get('shortDescription')
    #     fullDescription = request.POST.get('fullDescription')
    #     image = request.FILES.get('image')
    #     media = request.FILES.get('media')
    #     category = Category.objects.get(id=int(request.POST.get('category')))
    #     usersInTask = request.POST.getlist('listUsers')
    #     newTask = Task(
    #         title=title,
    #         shortDescription=shortDescription,
    #         fullDescription=fullDescription,
    #         image=image,
    #         media=media,
    #         category=category
    #     )
    #     newTask.save()
    #
    #     for user in usersInTask:
    #         userFromDB = User.objects.get(id=int(user))
    #         if userFromDB:
    #              newTask.users.add(userFromDB)
    #     newTask.save()
    #     return redirect('tutorTasksEdit', id=newTask.id)
