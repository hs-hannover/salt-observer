from django import template
register = template.Library()


@register.filter
def get(value, arg):
    return value.get(arg, '')
