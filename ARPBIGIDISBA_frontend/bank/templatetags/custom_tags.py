from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    """
    Devuelve getattr(obj, name), para extraer dinámicamente
    un atributo en un template.
    """
    return getattr(obj, name, '')