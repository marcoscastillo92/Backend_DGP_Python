from .models import MessageForumGroup
from users.models import User
from .models import ForumGroup
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
        forumQS = ForumGroup.objects.filter(id=idForum)
        if forumQS:
            forum = forumQS[0]
        else:
            forum= None 
        return forum
        
    def saveMessage(self, requestData):
        body = requestData['body']
        token = requestData['token']
        author = self.getAuthor(token)
        mimeType = requestData['mimeType']
        idforum = requestData['idForum']
        forum = self.getForum(idforum)

        if author and forum:
            messageToSave = MessageForumGroup(
                body = body,
                author = author,
                mimeType = mimeType,
                forum = forum,
            )
            messageToSave.save()
            response = json.loads('{"result": "success", "message": "Mensaje almacenado correctamente"}')
        elif not author:
            response = json.loads('{"result": "error", "message": "El usuario no existe"}')
        elif not forum:
            response = json.loads('{"result": "error", "message": "El foro no existe"}')
        return JsonResponse(response)

    def getMessages(self, requestData):
        messageType = requestData['messageType']
        if messageType == 'forumGroup':
            token = requestData['token']
            idForum = requestData['idForum']
            author = self.getAuthor(token)
            if author:
                forumGroup = ForumGroup.objects.filter(id=idForum)
                if forumGroup:
                    messagesForumGroup = list(MessageForumGroup.objects.filter(forum_id=forumGroup[0].id).values())
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