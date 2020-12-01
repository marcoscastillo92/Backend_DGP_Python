from django.shortcuts import redirect, render
from users.models import User, Pictograms
from forums.models import Forum
from groups.models import Groups
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.contrib.auth.hashers import check_password
import json
from users import forms as uForm
from users.controller import Controller as uController

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
                lista = Forum.objects.filter(identifier=identifier, emisorUser=userFromDB) | Forum.objects.filter(identifier=identifier, receptorUser=userFromDB)
            elif category == 'group':
                lista = Forum.objects.filter(identifier=identifier)
            myList = list(lista.order_by('createdAt').reverse())
            
           
            var = []
            for l in myList:
                print(l.id)
                if l.emisorUser_id:
                    user = User.objects.filter(id = l.emisorUser_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor_name": user[0].name, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path, "tutor": False}
                    var.append(respuesta)

                if l.emisorTutor_id:
                    user = Tutor.objects.filter(id = l.emisorTutor_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor_name": user[0].name, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path, "tutor": True}
                    var.append(respuesta)
            print(var)
            formatResponse = {"mensajes" : var}
            return JsonResponse(formatResponse, safe=False)
        else:
            response = {"result":"error", "message":"El usuario no existe"}
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
            #{idForum:int,messageType: "string",body:"string", mimeType}
            identifier = bodyData['identifier']
            forum = Forum.objects.filter(identifier = identifier, category="welcomeMessage") #mensaje creado por defecto
            if forum:
                body = bodyData['body']
                mimeType = bodyData['mimeType']
                category = bodyData['category']
                newForum = Forum(
                    body = body,
                    emisorTutor = None,
                    emisorUser = userFromDB,
                    receptorTutor = forum[0].emisorTutor, #obtener el tutor en la sesión,
                    receptorUser = None,
                    mimeType = mimeType,
                    category = category,
                    identifier = identifier
                )                
                newForum.save()
                response = {"result":"success", "message":"El mensaje se ha almacenado correctamente"}
                return JsonResponse(response, safe=False)
            else:
                response = {"result":"error", "message":"El foro no existe"}
                return JsonResponse(response, safe=False)
            messagesForum = list(Forum.objects.filter(id=idForum).values())
            return JsonResponse(messagesForum, safe=False)
        else:
            response = {"result":"error", "message":"El usuario no existe"}
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
        if not request.POST.get('username', False) or not  request.POST.get('password', False) :
            context = {}
            context['msg'] = '*Todos los campos son obligatorios'
            return render(request,'./tutors/index.html', context)
        else:
            tutorPass = Tutor.objects.filter(username= request.POST.get('username')).values('password')
            if tutorPass:
                if check_password(request.POST.get('password'),tutorPass[0]['password']) :
                    request.session['username'] = request.POST.get('username')
                    return redirect('/tutors/home')
                else:
                    context = {}
                    context['msg'] = '*Contraseña incorrecta'
                    return render(request,'./tutors/index.html', context)
            else:
                context = {}
                context['msg'] = '*El usuario no existe'
                return render(request,'./tutors/index.html', context) 

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

    