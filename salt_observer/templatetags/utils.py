from django import template
from django.utils.safestring import mark_safe

import hashlib
from markdown import Markdown
register = template.Library()


@register.filter
def get(value, arg):
    return value.get(arg, '')


@register.filter
def markdownify(value):
    return mark_safe(Markdown().convert(value))


@register.filter
def md5(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()
