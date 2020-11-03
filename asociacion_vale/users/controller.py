from users.models import User
class Controller:
    def eval(self, ):
        """
        docstring
        """
        pass
    def correctFiels(self, request, res, neededFields, allFields):
        missingFields = []
        extraFields = []
        msgErr = ""
        for neededField in neededFields:
            if (!eval('req.body.'+neededField)):
                missingFields.push(neededField)
        
        for key in req.body:
            if allFields.includes(key):
                extraFields.push(key)
        
        if(missingFields.length >0):
            msgErr = {"error" : "Missing fields", "missing_fields" : missing_fields}
            return JsonResponse(json.loads(msgErr))
        elif extraFields.length > 0:
            msgErr = {"error" : "Extra fields", "extra_fields" : extraFields};
            return JsonResponse(json.loads(msgErr))
        else:
            return True

        return False
    def userLogin(request):
        neededUserLoginFields = ["password"]
        allUserLoginFields = ["password"]
        if  correctFiels(req, res, neededUserLoginFields, allUserLoginFields):
            bodyUnicode = request.body.decode('utf-8')
            userData = json.loads(bodyUnicode)
            userFromDB = User.objects.filter(password=userData['password'])
            if userFromDB:
                response = {result: "success", token: userFromDB['token']}
                request.session.user = userFromDB
                request.session.token = response.token
                return JsonResponse(json.loads(response))
            else:
                response = {result: "error", message: 'User not registred'}
                return JsonResponse(json.loads(response))