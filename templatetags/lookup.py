# coding=utf-8
from django import template

register = template.Library()


@register.filter(name='shift_to_name')
def shift_to_name(value, arg, default=""):
    try:
        return value[arg].shift_knd.short_name
    except:
        return ""


@register.filter(name='shift_to_cssclass')
def shift_to_cssclass(value, arg, default=""):
    try:
        return value[arg].shift_knd.css_class
    except:
        return ""
