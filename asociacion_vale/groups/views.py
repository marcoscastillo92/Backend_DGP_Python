from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Groups, Category
from forums.models import Forum
import json

# Create your views here.
@csrf_exempt
def index(request):
    pass

@csrf_exempt
def groupsCreate(request):
    if request.method == 'POST':
        groupData = json.loads(request.body)
        group = Groups(
            name= groupData['name'],
        )
        group.save(idCategory=groupData['category'])
        forum = Forum.objects.filter(idTarget=group)
        if not forum:
            forum = Forum(idTarget=group)
            forum.save()
        string = '{"Name":"'+groupData['name']+'", "Category":"'+str(groupData['category'])+'"}'
    return JsonResponse(json.loads(string))

@csrf_exempt
def groupsGet(request, id):
    pass

@csrf_exempt
def categoryCreate(request):
    if request.method == 'POST':
        categoryData = json.loads(request.body)
        group = Category(
            name= categoryData['name']
        )
        group.save()
        string = '{"Name":"'+categoryData['name']+'"}'
    return JsonResponse(json.loads(string))