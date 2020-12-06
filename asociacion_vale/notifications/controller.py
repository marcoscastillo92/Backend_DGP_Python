from .models import Notifications
from users.models import User
from pyfcm import FCMNotification


class Controller:
    def sendNotication(id,type,group=None,task=None):
        if type == 'task':
            user = User.objects.get(id = id)
            tokenDevice = user.deviceToken
            if tokenDevice != None or tokenDevice != "":
                push_service = FCMNotification(api_key=user.apiKey)
                registration_id = tokenDevice
                message_title = "Nueva tarea"
                message_body = "Tienes una nueva tarea asignada"
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

        if type== "messageGroup":
            user = User.objects.get(id = id)
            tokenDevice = user.deviceToken
            if tokenDevice != None or tokenDevice != "":
                push_service = FCMNotification(api_key=user.apiKey)
                registration_id = tokenDevice
                message_title = "Nuevo Mensaje en el grupo " + group
                message_body = "Hay mensajes nuevos en el grupo" + group
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

        if type== "messageTask":
            user = User.objects.get(id = id)
            tokenDevice = user.deviceToken
            if tokenDevice != None or tokenDevice != "":
                push_service = FCMNotification(api_key=user.apiKey)
                registration_id = tokenDevice
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