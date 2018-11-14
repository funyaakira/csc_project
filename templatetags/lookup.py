# coding=utf-8
from django import template
register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg, default=""):
    return value[arg]
    # if arg in value:
    #     return value[arg]
    # else:
    #     return default
