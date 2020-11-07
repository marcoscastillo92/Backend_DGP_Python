from django.shortcuts import render
from .controller import Controller
# Create your views here.
@csrf_exempt
def postMessage(request):
    controller = Controller()
    if request.method == 'POST':
        bodyUnicode = request.body.decode('utf-8')
        requestData = json.loads(bodyUnicode)

        userFromDB = list(User.objects.filter(password=requestData['password']).values())
        