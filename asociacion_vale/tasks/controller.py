from .models import MessageForum
class Controller:
    def messageManagement(self, request):
        bodyUnicode = request.body.decode('utf-8')
        requestData = json.loads(bodyUnicode)

        #Publicar un mensaje tipo forum
        if requestData['messageType'] == 'forum':
            
        pass