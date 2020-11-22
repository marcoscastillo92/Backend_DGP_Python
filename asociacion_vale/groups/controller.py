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

    def createGroup(self, request):
        if request.session.get('username', False):
            nameGroup = request.POST.get('groupName')
            usersInGroup = request.POST.getlist('listUsers')
            tutor = Tutor.objects.filter(username=request.session.get('username'))
            identifier = secrets.token_hex(10)
            newGroup = Groups(
                name=nameGroup,
                identifier = identifier,
                memberCount = len(usersInGroup)
            )
            newGroup.save()
            newGroup.tutors.set(tutor)

            arrayUser = []
            for user in usersInGroup:
                userFromDB = User.objects.get(username=user)
                if userFromDB:
                     newGroup.users.add(userFromDB)
            return redirect('/tutors/groups')

    def deleteGroup(self, request):
        if request.session.get('username', False):
            groupIdentifier = request.POST.get('groupIdentifier')
            if groupIdentifier:
                groupFromDB = Groups.objects.filter(identifier=groupIdentifier)
                if groupFromDB:
                    groupFromDB.delete()
            return redirect('/tutors/groups')

    def chatGroup(self, request):
        if request.session.get('username', False):
            context = {}
            asociacion_valeController = ascController()
            messages = asociacion_valeController.getMessagesTutors(request)
            identifier = request.GET.get('identifier')
            if identifier:
                groupFromDB = Groups.objects.filter(identifier=identifier)
                context['group'] = groupFromDB[0]
            if messages:
                context['messages'] = messages
            context['tutor'] = request.session.get('username')
            return render(request,'./tutors/chatGroup.html', context)
        else:
            return redirect('/tutors/groups')        
 
    def editGroup(self,request):
        if request.GET.get('identifier',False):
            id = request.GET.get('identifier',False)
            group = Groups.objects.get(identifier= id)
            usersIngroup = group.users.all()
           
            context = {}
            context['info'] = group
            context['usersIn'] = usersIngroup
            usersGroups = usersIngroup.values()
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
                            print("Borrando a" )
                            print(j['username'])
                            usersOut.pop(i)
                            break
                break
            return  render(request, './tutors/editGroup.html', context)

       