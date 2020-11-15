from .models import Groups, MessageForumGroup
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
        
    def saveMessage(self, request):
        bodyUnicode = request.body.decode('utf-8')
        requestData = json.loads(bodyUnicode)
        body = requestData['body']
        token = request.META['HTTP_AUTHORIZATION']
        author = self.getAuthor(token)
        mimeType = requestData['mimeType']
        idforum = requestData['idForum']
        forum = self.getForum(idforum)

        if author and forum:
            messageToSave = MessageForumGroup(
                body = body,
                author = author,
                mimeType = mimeType,
                group = forum,
            )
            messageToSave.save()
            response = json.loads('{"result": "success", "message": "Mensaje almacenado correctamente"}')
        elif not author:
            response = json.loads('{"result": "error", "message": "El usuario no existe"}')
        elif not forum:
            response = json.loads('{"result": "error", "message": "El foro no existe"}')
        return JsonResponse(response)

    def getMessages(self, request):
        body_unicode = request.body.decode('utf-8')
        requestData = json.loads(body_unicode)
        
        messageType = requestData['messageType']
        if messageType == 'forumGroup':
            token =  request.META['HTTP_AUTHORIZATION']
            idForum = requestData['idForum']
            author = self.getAuthor(token)
            if author:
                forumGroup = Groups.objects.filter(id=idForum)
                if forumGroup:
                    messagesForumGroup = list(MessageForumGroup.objects.filter(group_id=forumGroup[0].id).values())
                    if messagesForumGroup:
                        return JsonResponse(messagesForumGroup, safe=False)
                    else:
                        response = json.loads('{"result": "error", "message": "El foro no contiene ningún mensaje"}')
                        return JsonResponse(response)    
                else:
                    response = json.loads('{"result": "error", "message": "El foro no existe"}')
                    return JsonResponse(response)
            else:
                response = json.loads('{"result": "error", "message": "El usuario no existe"}')
                return JsonResponse(response)


    def getGroups(self,request):
        tokenUser= request.META['HTTP_AUTHORIZATION']
        user = User.objects.filter(token=tokenUser)
        if user:
            userId= user[0].id
            myQuery = Groups.objects.filter(users__id = userId)
            groups = list(myQuery.values('name','memberCount', 'id'))
            return JsonResponse(groups, safe=False)
        else:
            response = json.loads('{"result": "error", "message": "El usuario no existe"}')
            return JsonResponse(response)