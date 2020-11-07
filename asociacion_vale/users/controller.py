#from asociacion_vale.users.views import pictograms
from json.decoder import JSONDecoder
from .models import User
from django.http import JsonResponse
import json
import secrets
from .models import Pictograms
import datetime

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
        if  self.correctFields(request, neededUserLoginFields, allUserLoginFields):
            bodyUnicode = request.body.decode('utf-8')
            userData = json.loads(bodyUnicode)
            userFromDB = list(User.objects.filter(password=userData['password']).values())
            if userFromDB:
                userData = userFromDB[0]
                #response = json.dumps('{"result": "success", "token": userFromDB["token"]}')
                response = {'result':'success', 'token': userData['token']}
                request.session.user = userData
                print(response['token'])
                request.session.token = response['token']
                return JsonResponse(response, safe=False)
            else:
                #response = json.loads('{"result": "error", "message": "User not registred"}')
                response = {'result':'error', 'message': 'User not registred'}
                #response.status_code = 404
                return JsonResponse(response, safe=False)

    def getPictograms(self, request):
        pictograms = list(Pictograms.objects.values())
        return JsonResponse(pictograms, safe=False)

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
            name= "cerdo",
            key= secrets.token_hex(15),
        )
        newPictogram.save()
        
        newPictogram = Pictograms(
            name= "perro",
            key= secrets.token_hex(15),
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "gato",
            key= secrets.token_hex(15),
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "delfin",
            key= secrets.token_hex(15),
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "leon",
            key= secrets.token_hex(15),
        )
        newPictogram.save()

        newPictogram = Pictograms(
            name= "caballo",
            key= secrets.token_hex(15),
        )
        newPictogram.save() 
        response = json.loads('{"result": "success", "message": "Pictogramas introducidos correctamente"}')
        return JsonResponse(response)

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
        return JsonResponse(randomUser, safe=False)


    def  getUserInfobyId(self, request, id):
        id = id
        try:
            response = User.objects.filter(_id=id)
        except:
            response =  json.loads('{"error": "UsernotFound"}')
            #request.status = 404
        
        return JsonResponse(response)
        
        
    


    
""" 
/**
 * @author Jose
 * @params: User es el objeto usuarioq ue se obntiene de la bd
 * @return: retorna el JSON con el objeto Usuario.
 */
async function getUserInfoById(req, res) {
    var id = req.params.id;
    try{
        var user = await User.findById(id);
    }catch{
        user = {"error": "UserNotFound"};
        Logger.addLog('userController', 'User not found', {'id': id, 'requestParams': req.params});
        res.status(404).send(user);
    }
    res.send(user);
}

/**
 * Fn que crea un usuario con unos datos mínimos especificados
 * @author Marcos
 * @param {*} req
 * @param {*} res
 * @return new user object or json with missing fields
 */
async function createUser(req, res){
    delete req.body.token;
    if(correctFields(req, res, neededUserFields, allUserFields)){
        var userData = req.body;
        userData.role = userData.role.toLowerCase();
        //userData.password = bcrypt.hashSync(userData.password, bcrypt.genSaltSync(10));
        var newUser = await new User(userData);
        newUser.save((err, result) =>{
            if(err) Logger.addLog('userController', 'Creation error', {'error': err, 'userObject': result, 'requestBody': userData});
            else Logger.addLog('userController', 'User created', {'userObject': result, 'requestBody': userData});
        });
        res.send(newUser);
    }
}
 """