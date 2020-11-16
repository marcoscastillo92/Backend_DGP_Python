from users.models import User
from forums.models import Forum
from django.http import JsonResponse
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
            messagesForum = list(Forum.objects.filter(identifier=identifier).values())
            return JsonResponse(messagesForum, safe=False)
        else:
            response = {"result":"error", "message":"El usuario no existe"}
            return JsonResponse(response, safe=False)
    
    def postMessage(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        userFromDB = self.getUserByToken(token)
        if userFromDB:
            bodyData = json.loads(request.body)
            #{idForum:int,messageType: "string",body:"string", mimeType}
            identifier = bodyData['identifier']
            forum = Forum.objects.filter(identifier = identifier) #mensaje creado por defecto
            if forum:
                body = bodyData['body']
                mimeType = bodyData['mimeType']
                category = bodyData['category']
                newForum = Forum(
                    body = body,
                    tutor = forum[0].tutor,
                    author = userFromDB,
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
