from django.template.library import Library

register = Library()


@register.simple_tag
def getStatus(array):
    array = [array]
    response = ''
    count = 0
    for value in array:
        if value:
            status = "Completado" if value[count].get('status') else "En progreso"
            response += f"{value[count].get('user')} | {status}\n"
        count = count + 1
    return response


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
