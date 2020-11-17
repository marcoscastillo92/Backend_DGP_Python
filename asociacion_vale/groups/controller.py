from .models import Groups
from users.models import User
from django.http import JsonResponse


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