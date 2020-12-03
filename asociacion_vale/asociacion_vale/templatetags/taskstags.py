from django.template.library import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def getStatus(array):
    html = '<div class="container">'
    for value in array:
        user = array[value].get('user')
        status = array[value].get('status')
        profileImage = user.profileImage.url if user.profileImage else "static/img/profile.png"
        checked = "checked" if status.done else ""
        statusMsg = "Completado" if status.done else "En progreso"
        html += f'''
        <div class="row align-items-center" id="resultados_{user.id}">
                <div class="col-sm">
                    <img style="width: 50px;" src="/{profileImage}">
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
