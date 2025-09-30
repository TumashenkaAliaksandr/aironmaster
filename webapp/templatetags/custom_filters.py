import html

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def batch(value, n):
    n = int(n)
    return [value[i:i + n] for i in range(0, len(value), n)]


@register.filter(name='splitlines')
def splitlines(value):
    if value:
        return value.splitlines()
    return []


@register.filter
def html_unescape(value):
    if value:
        unescaped = html.unescape(value)
        return mark_safe(unescaped)
    return value
