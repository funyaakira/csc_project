# coding=utf-8
from django import template
from ..libs.funcs import seireki_to_wareki as libs_seireki_to_wareki
from ..libs.funcs import calculate_age as libs_calculate_age
from .. import models

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


@register.filter(name='seireki_to_wareki')
def seireki_to_wareki(value):
    return libs_seireki_to_wareki(value);


@register.filter(name='calculate_age')
def calculate_age(value):
    return libs_calculate_age(value);


@register.filter(name='get_events')
def get_events(evnets, date):
    return evnets.filter(date=date)


@register.filter(name='get_kirokus_day')
def get_kirokus_day(kirokus, date):
    return kirokus.filter(exec_date=date).order_by('date', 'time')

# 記録のオブジェクトリストを聞き数に
@register.filter(name='get_kirokus_riyosya')
def get_kirokus_riyosya(kirokus, riyosya):
    return kirokus.filter(riyosya=riyosya).order_by('date', 'time')
