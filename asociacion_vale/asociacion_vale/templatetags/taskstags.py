from django.template.library import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def getStatus(array):
    array = [array]
    html = '<div class="container">'
    count = 0
    for value in array:
        user = array[value].get('user')
        status = array[value].get('status')
        profileImage = user.profileImage.url if user.profileImage else "static/img/profile.png"
        checked = "checked" if status.done else ""
        statusMsg = "Completado" if status.done else "En progreso"
        html += f'''
        <div class="row align-items-center" id="resultados_{user.id}">
                <img style="width: 50px;" src="/{profileImage}">
                <div class="col-sm">
                    <img style="width: 50px;" src="/{user.profileImage.url}"> 
                </div>
                <div class="col-sm">
                    <a href="/tutors/users/edit/{user.id}">{user.name}</a> <br> {statusMsg} 
                </div>
                <div class="col-sm">
                    <form action="/tasks/status" method="POST"><label><input type="hidden" id="taskId" name="taskId" value="{status.id}"><input type="checkbox" id="resuelto{user.id}" name="done" value="1" {checked}> Resuelto</label><input type="submit" value="Actualizar"></form>
                </div>
                <div class="col-sm">
                    <a href="/tutors/tasks/chat/{status.task.identifier}">Chat</a>
                </div>
            </div>
            '''
        count = count + 1
        html += '</div>'
    return mark_safe(html)


@register.simple_tag
def getRatings(array):
    array = [array]
    response = ''
    count = 0
    for value in array:
        if value:
            response += f"{value[count].get('user')} | {value[count].get('text')} | Dificultad: {value[count].get('difficulty')}/5 | Utilidad: {value[count].get('utility')}/5 \n"
        count = count + 1
    return response
