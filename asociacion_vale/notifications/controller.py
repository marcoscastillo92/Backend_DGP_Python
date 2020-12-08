from .models import Notifications
from users.models import User
from pyfcm import FCMNotification


class Controller:
    def sendNotication(self, id,type,group=None,task=None):
        user = User.objects.get(id=id)
        tokenDevice = user.deviceToken
        if tokenDevice != None and tokenDevice != "":
            push_service = FCMNotification(api_key="AAAAJPDrl-c:APA91bEKWQANHQcSQrkAlPOtN7rrGZ3VpyC1Zf17dCjCpCIZM6YCQ6unj4MFlOulo6dsXmmXFKWuSaSt-HE4JtqTJ675zPkYBNTtwvuUyXtqhQq74oTSzD85o4ZrVn9cTLphQEnlNjWb")
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

            notification = Notifications(
                messageTitle = message_title,
                messageBody =  message_body
            )
            notification.save()
            notification.user.add(user)

            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

            if result:
                return True
            else:
                return False