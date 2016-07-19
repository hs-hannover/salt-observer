from django import template
from django.utils.safestring import mark_safe

from markdown import Markdown
register = template.Library()


@register.filter
def get(value, arg):
    return value.get(arg, '')


@register.filter
def markdownify(value):
    return mark_safe(Markdown().convert(value))
