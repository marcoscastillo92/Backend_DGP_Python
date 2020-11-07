from .models import MessageForum
from .models import User
from .models import Forum
from django.http import JsonResponse
import json
class Controller:
    def getAuthor(self, token):
        author = MessageForum.objects.filter(token=token)
        #author = json.loads(authorQS)
        objectAuthor = User(
            name = author["name"],
            email = author['email'],
            username = author['username'],
            password = author['password'],
            phoneNumber = author['phoneNumber'],
            profileImage = author['profileImage'],
            birthDate = author['birthDate'],
            token = author['token'],
            gender = author['gender'],
            createdAt = author['createdAt'],
            )
        return objectAuthor

    def getForum(self, idForum):
        forum = MessageForum.objects.filter(_id=idForum)
        #forum = json.loads(forumQS)
        objectforum = User(
            name = forum["name"],
            createdAt = forum['createdAt'],
            )
        return objectforum