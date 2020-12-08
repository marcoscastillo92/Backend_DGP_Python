from asociacion_vale.settings import API_KEY
from .models import Notifications
from users.models import User
from pyfcm import FCMNotification


class Controller:
    def sendNotication(self, id,type,group=None,task=None):
        user = User.objects.get(id=id)
        tokenDevice = user.deviceToken
        if tokenDevice != None and tokenDevice != "":
            push_service = FCMNotification(api_key=API_KEY)
            registration_id = tokenDevice

            if type == 'task':
                message_title = "Nueva tarea"
                message_body = "Tienes una nueva tarea asignada"
            if type== "messageGroup":
                message_title = "Nuevo Mensaje en el grupo " + group
                message_body = "Hay mensajes nuevos en el grupo" + group
            if type== "messageTask":
                message_title = "Nuevo Mensaje en la tarea " + task
                message_body = "Tienes un nuevo mensaje en la tarea " + task
            if type == "finishedTask":
                message_title = "Has finalizado la tarea " + task
                message_body = "Has finalizado la tarea " + task

            notification = Notifications(
                messageTitle=message_title,
                messageBody= message_body,
                apiKey=API_KEY
            )
            notification.save()
            notification.user.add(user)

            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            if result:
                return True
            else:
                return False