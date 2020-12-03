from .models import Groups
from users.models import User
from forums.models import Forum
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.shortcuts import redirect
from asociacion_vale.controller import Controller as ascController
from django.shortcuts import redirect, render
import secrets
import json
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

class Controller:
    def getAuthor(self, token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

    def getForum(self, idForum):
        forumQS = Groups.objects.filter(id=idForum)
        if forumQS:
            forum = forumQS[0]
        else:
            forum= None 
        return forum

    def getGroups(self,request):
        tokenUser= request.META['HTTP_AUTHORIZATION']
        user = User.objects.filter(token=tokenUser)
        if user:
            userId= user[0].id
            myQuery = Groups.objects.filter(users__id = userId)
            groups = list(myQuery.values('name','memberCount', 'identifier'))
            response = {"grupos" : groups}
            return JsonResponse(response, safe=False)
        else:
            response = json.loads('{"result": "error", "message": "El usuario no existe"}')
            return JsonResponse(response)

  

    def deleteGroup(self, request):
        if request.session.get('username', False):
            groupIdentifier = request.POST.get('identifier')
            if groupIdentifier:
                groupFromDB = Groups.objects.filter(identifier=groupIdentifier)
                if groupFromDB:
                    groupFromDB.delete()
            return redirect('/tutors/groups')

    def getChatGroup(self, request, id):
        if request.method == 'GET':
            context = {}
            asociacion_valeController = ascController()
            messages = asociacion_valeController.getMessagesTutors(id)
            groupFromDB = Groups.objects.filter(identifier=id)
            context['group'] = groupFromDB[0]
            if messages:
                context['messages'] = messages
            context['tutor'] = request.session.get('username')
            return render(request,'./tutors/chatGroup.html', context)
        else:
            return redirect('/tutors/groups')        
 
    def editConfirmGroup(self, request):
        if request.session.get('username', False):
            nameGroup = request.POST.get('name')
            identifier = request.POST.get('identifier')
            usersInGroup = request.POST.getlist('listUsers')
            if identifier:
                groupFromDB = Groups.objects.get(identifier = identifier)
                if groupFromDB:
                    groupFromDB.name = nameGroup
                    groupFromDB.memberCount = len(usersInGroup)
                    groupFromDB.save()
                    
                    # NOTIFICACIONES
                    # grupoInfo = groupFromDB
                    # usuarios = groupFromDB.users 
                    # 
                    # for u in usuarios:
                    #   for user in usersInGroup:
                    #       if u == user:
                    #           esta= True
                    #   if !esta:
                    #      sendNotificacion 
                    # 
                    groupFromDB.users.clear()
                    for user in usersInGroup:   
                        userFromDB = User.objects.get(id=user)
                        if userFromDB:
                            groupFromDB.users.add(userFromDB)
                    groupFromDB.save()
               
                return redirect('/tutors/groups')

    def createConfirmGroup(self, request):
        if request.session.get('username', False):
            print(request.POST)
            nameGroup = request.POST.get('name')
            usersInGroup = request.POST.getlist('listUsers')
            tutor = Tutor.objects.filter(username=request.session.get('username'))
            identifier = secrets.token_hex(10)
            newGroup = Groups(
                name=nameGroup,
                memberCount = len(usersInGroup),
                identifier = identifier
            )
            newGroup.save()
            newGroup.tutors.set(tutor)
            print(identifier)
            for userId in usersInGroup:
                userFromDB = User.objects.get(id=userId)
                if userFromDB:
                     newGroup.users.add(userFromDB)
            return redirect('/tutors/groups')

    def editGroup(self, request, id):
        if request.method == 'GET':
            group = Groups.objects.get(identifier=id)
            usersInGroup = group.users.all()
            context = {}
            context['info'] = group
            context['usersIn'] = usersInGroup
            usersGroups = usersInGroup.values()
            allUsers = list(User.objects.all().values())
            usersOut = []
            usersIn = []

            for i in usersGroups:
                usersIn.append(i)
                
            for i in allUsers:
                usersOut.append(i)

            context ['userOut'] = usersOut
            context ['userIn'] = usersIn

            for i in range(len(usersOut)):
                for j in usersIn:
                    for key , value in usersOut[i].items():
                        if key=="username" and value == j['username']:
                            usersOut.pop(i)
                            break
                break
            return  render(request, './tutors/editGroup.html', context)

    def editGroupOld(self, request, id):
        if request.method == 'GET':
            group = Groups.objects.get(identifier=id)
            usersInGroup = group.users.all()
            context = {}
            context['info'] = group
            context['usersIn'] = usersInGroup
            usersGroups = usersInGroup.values()
            allUsers = list(User.objects.all().values())
            usersOut = []
            usersIn = []

            for i in usersGroups:
                usersIn.append(i)
                
            for i in allUsers:
                usersOut.append(i)

            context ['userOut'] = usersOut
            context ['userIn'] = usersIn

            for i in range(len(usersOut)):
                for j in usersIn:
                    for key , value in usersOut[i].items():
                        if key=="username" and value == j['username']:
                            usersOut.pop(i)
                            break
                break
            return  render(request, './tutors/editGroup.html', context)

    def postMessageGroup(self, request):
        controller = ascController()
        if controller.postMessageTutor(request):
            return redirect('/tutors/groups/chat/get/'+ request.POST.get('identifier'))

    def createGroup(self, request):
        if request.method == 'GET':
            usersFromDB = list(User.objects.all().order_by('name').values())
            context = {"userOut" : usersFromDB}
            return render(request, './tutors/createGroup.html', context)