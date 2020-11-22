from .models import Groups
from users.models import User
from forums.models import Forum
from django.http import JsonResponse
from django.contrib.auth.models import User as Tutor
from django.shortcuts import redirect
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
        if request.session.get('username',False):
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
                    
            print(tutor)
            print(request.POST)
            return redirect('/tutors/groups')