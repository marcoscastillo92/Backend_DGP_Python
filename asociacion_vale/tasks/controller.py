from .models import Rating, Task, Progress
from users.models import User
import json

class Controller:
    def messageManagement(self, request):
        bodyUnicode = request.body.decode('utf-8')
        requestData = json.loads(bodyUnicode)

        #Publicar un mensaje tipo forum
        if requestData['messageType'] == 'forum':
           print() 
        pass

    def createTask(self, request):
        if request.method == 'POST':
            task = Task(request.body)
            task.save()
    
    def assignTask(self, request):
        if request.method == 'POST':
            task = Task.objects.get(id=request.body.taskId)
            user = User.objects.get(id=request.body.userId)
            userProgress = Progress.objects.all(user=user, category = task.category)
            progress = Progress(user=user, category = task.category, total=userProgress.lenght+1)