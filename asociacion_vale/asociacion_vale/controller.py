from django.shortcuts import redirect, render
from users.models import User
from forums.models import Forum
from groups.models import Groups
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.contrib.auth.hashers import check_password
import json
from users import forms as uForm
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
                    respuesta = {"body":l.body, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path}
                    var.append(respuesta)

                if l.emisorTutor_id:
                    user = Tutor.objects.filter(id = l.emisorTutor_id)
                    print(user[0].username)
                    respuesta = {"body":l.body, "emisor":user[0].username,  "created":l.createdAt, "identifier":l.identifier, "mimeType":l.mimeType.path}
                    var.append(respuesta)
            print(var)
            formatResponse = {"mensajes" : var}
            return JsonResponse(formatResponse, safe=False)
        else:
            response = {"result":"error", "message":"El usuario no existe"}
            return JsonResponse(response, safe=False)

    def getMessagesTutors(self, request):
            identifier = request.GET.get('identifier')
            lista = Forum.objects.filter(identifier=identifier)
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
        listUsers = list(User.objects.all().values())

        if listUsers:
            arrayUsers = []
            for user in listUsers:
                arrayUsers.append(user)
        context['users'] = arrayUsers
        return render(request,'./tutors/users.html', context)
            

    def tutorsUsersEdit(self,request,id):
        infoUser = User.objects.get(id=id)
        userForm = uForm.userForm(request.POST or None, request.FILES or None, instance=infoUser)
        userForm.fields['image'].required = False
        userForm.fields['media'].required = False
        context = {'task': infoUser, 'form': userForm}
        if request.method == 'POST':
            # Guardar cambios
            if userForm.is_valid():
                userForm.save()
                return render(request, 'tutors/task-detail.html', context)
        return render(request, 'tutors/task-detail.html', context)