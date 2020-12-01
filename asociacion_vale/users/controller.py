#from asociacion_vale.users.views import pictograms
from json.decoder import JSONDecoder
from .models import User
from django.http import JsonResponse
import json
import secrets
from .models import Pictograms
from datetime import date

NEEDED_USERS_FIELDS =  ["name","username","password","role"]
ALL_USERS_FIELDS =  ["name","username","password","role","email","phoneNumber","birthDay"]
NEEDED_USER_LOGIN_FIELDS = ["password"]
ALL_USER_LOGIN_FIELDS = ["password"]

class Controller:
         
    def correctFields(self, request, neededFields, allFields):
        missingFields = []
        extraFields = []
        msgErr = ""
        userData = json.loads(request.body)
        for neededField in neededFields:
            if not eval('userData["'+neededField+'"]'):
                missingFields.push(neededField)
        
        for key in request.body:
            if key in allFields:
                extraFields.push(key)
        
        if(len(missingFields) > 0):
            response = json.dumps({"error" : "Missing fields", "missing_fields" : missingFields})
            #response.status_code = 400
            return response
        elif len(extraFields) > 0:
            response = json.dumps({"error" : "Extra fields", "extra_fields" : extraFields})
            #response.status_code = 400
            return response
        else:
            return True

        return False

    def usersLogin(self, request):
        neededUserLoginFields = ["password"]
        allUserLoginFields = ["password"]
        if self.correctFields(request, neededUserLoginFields, allUserLoginFields):
            bodyUnicode = request.body.decode('utf-8')
            userData = json.loads(bodyUnicode)
            userFromDB = User.objects.get(password=userData['password'])
            if userFromDB:
                userFromDB.token = secrets.token_hex(64)
                userFromDB.save()
                response = {'result':'success', 'token': userFromDB.token}
                request.session.user = userFromDB
                request.session.token = response['token']
                return JsonResponse(response, safe=False)
            else:
                response = {'result':'error', 'message': 'User not registred'}
                return JsonResponse(response, safe=False)

    def getPictograms(self, request):
        pictograms = list(Pictograms.objects.values())
        if not len(pictograms):
            print("Introduciendo pictogramas")
            self.savePictograms(request)

        pictograms = list(Pictograms.objects.values())
        if pictograms:
            response = {"pictograms": pictograms}
        return JsonResponse(response, safe=False)

    def generatePassword(self,request):
        pictograms = self.getPictograms(request)
        possibleKeys = []
        possibleNames = []

        for x in pictograms:
            array = json.loads(x)
            for index in range(len(array)):
                possibleKeys.append(array[index]["key"])
                possibleNames.append(array[index]["name"])
            
        password = ""
        secret = 0
        names = ""
        for i in range(len(possibleKeys)):
           secret = secrets.randbelow(len(possibleKeys))
           password +=  possibleKeys[secret] #Se obtiene una key aleatoria
           names += " " + possibleNames[secret]
    
        response = {"names" : names,"password" : password}
        return JsonResponse(response, safe=False)
        
    def savePictograms(self, request):
        newPictogram = Pictograms(
            name= "Avion",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/avion.png",
        )
        newPictogram.save()
        
        newPictogram = Pictograms(
            name= "Casa",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/casa.png",
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "Coche",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/coche.png",
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "Libro",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/libro.png",
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "Llaves",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/llaves.png",
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "Perro",
            key= secrets.token_hex(15),
            image="static/uploads/img/pictograms/perro.png",
        )
        newPictogram.save() 

    def saveRandomUser(self, request):
        newUser = User(
            name="Marcos Castillo",
            email= "marcos@gmail.com",
            username= "marcos",
            password= "c11a1b10acd84d5aa0e2290096603cc11a1b10acd84d5aa0e2290096603cc11a1b10acd84d5aa0e2290096603cc11a1b10acd84d5aa0e2290096603cc11a1b10acd84d5aa0e2290096603cc11a1b10acd84d5aa0e2290096603c",
            phoneNumber= "615234521",
            token= "11a1b10acd84d5aa0e2290096603cc"
        )
        newUser.save()
        response = json.loads('{"result": "success", "message": "Usuario creado correctamente"}')
        return JsonResponse(response)

    def getRandomUser(self, request):
        randomUser = list(User.objects.filter(email="marcos@gmail.com").values())
        if randomUser:
            response = {"user": randomUser[0]}
        return JsonResponse(response, safe=False)


    def  getUserInfobyId(self, request, id):
        id = id
        try:
            response = User.objects.filter(_id=id)
        except:
            response =  json.loads('{"error": "UsernotFound"}')
            #request.status = 404
        
        return JsonResponse(response)
        
    def getUserByToken(self, token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

    def getForum(self, idForum):
        forumQS = ForumUser.objects.filter(id=idForum)
        if forumQS:
            forum = forumQS[0]
        else:
            forum= None 
        return forum
    
    def saveMessage(self, requestData):
        body = requestData['body']
        token = requestData['token']
        author = self.getUserByToken(token)
        mimeType = requestData['mimeType']
        idforum = requestData['idForum']
        forum = self.getForum(idforum)

        if author and forum:
            messageToSave = MessageForumUser(
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
    
    def getUserByToken(self, token):
        authorQS = User.objects.filter(token=token)
        if authorQS:
            author = authorQS[0]
        else:
            author = None
        return author

    def getMessages(self, requestData):
        messageType = requestData['messageType']
        if messageType == 'forumUser':
            token = requestData['token']
            tutorId = requestData['idTutor']
            author = self.getUserByToken(token)
            if author:
                forumUser = ForumUser.objects.filter(user_id=author.id, tutor_id=tutorId)
                if forumUser:
                    messagesForumUser = list(MessageForumUser.objects.filter(forum_id=forumUser[0].id).values())
                    if messagesForumUser:
                        return JsonResponse(messagesForumUser, safe=False)
                    else:
                        response = json.loads('{"result": "error", "message": "El foro no contiene ningún mensaje"}')
                        return JsonResponse(response)    
                else:
                    response = json.loads('{"result": "error", "message": "El foro no existe"}')
                    return JsonResponse(response)
            else:
                response = json.loads('{"result": "error", "message": "El usuario no existe"}')
                return JsonResponse(response)

        
    def getUserProfile(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        userFromDB = self.getUserByToken(token)
        if userFromDB:
            today = date.today()
            calculatedAge = today.year - userFromDB.birthDate.year - ((today.month, today.day) < (userFromDB.birthDate.month, userFromDB.birthDate.day))
            response = {"user": {"name": userFromDB.name, "age": calculatedAge, "username": userFromDB.username, "genre": userFromDB.gender, "image": ""}}
            return JsonResponse(response, safe=False)
        else:
            response = {"result":"error", "message":"El usuario no existe"}
            return JsonResponse(response, safe=False)

    #Borra el token asociado al usuario, lo pone a null
    def userLogout(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        userFromDB = self.getUserByToken(token)
        userFromDB.token = "null"
        userFromDB.save()
        if userFromDB and userFromDB.token=="null":
            response = {"result":"success", "message":"Se ha realizado el logout correctamente"}
            return JsonResponse(response, safe=False)
        else:
            response = {"result":"error", "message":"No se ha podido realizar el logout correctamente"}
            return JsonResponse(response, safe=False)
