from django.template.library import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def getStatus(array):
    html = '<div class="container">'
    for value in array:
        user = array[value].get('user')
        status = array[value].get('status')
        statusMsg = "Completado" if status.done else "En progreso"
        checked = "checked" if status.done else ""
        html += f'''
        <div class="row align-items-center" id="resultados_{user.id}">
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
                <a href="/tutors/tasks/chat/{status.task.identifier}/{user.id}"><img style="width: 50px;" src="/static/img/chat.png"> </a>
            </div>
        </div>
        <hr/>
        '''
    html += '</div>'
    return mark_safe(html)


@register.simple_tag
def getRatings(array):
    response = ''
    html = '<div class="container">'
    for value in array:
        html += f'''
            <div class="row align-items-center" id="valoracion_{array[value].get('user').username}">
                <div class="col-sm">
                    {array[value].get('user')}
                </div>
                <div class="col-sm">
                    {array[value].get('text')}
                </div>
                <div class="col-sm">
                    Dificultad: {array[value].get('difficulty')}/5
                </div>
                <div class="col-sm">
                    Utilidad: {array[value].get('utility')}/5
                </div>
            </div>
            '''
    html += '</div>'
    return response
