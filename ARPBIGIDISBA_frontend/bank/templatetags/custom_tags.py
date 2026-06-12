from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    """Returns getattr(obj, name) to dynamically access an attribute in a template."""
    return getattr(obj, name, '')