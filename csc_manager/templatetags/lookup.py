# coding=utf-8
from django import template
from django.conf import settings
from django.db.models import Q, Case, When, IntegerField, TimeField

from datetime import datetime, date, timedelta

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
    return kirokus.filter(exec_date=date).order_by('date', 'disp_time')


@register.filter(name='get_kirokus_riyosya')
def get_kirokus_riyosya(kirokus, riyosya):
    return kirokus.filter(riyosya=riyosya).order_by('date', 'disp_time')


@register.filter(name='get_gender_name')
def get_gender_name(id):
    id -= 1 # indexを合わせるため1引く…
    return models.gender[id][1]


@register.filter(name='get_yokaigodo_name')
def get_yokaigodo_name(id):
    id -= 1 # indexを合わせるため1引く…
    return models.youkaigodo[id][1]


@register.filter(name='get_bed_count')
def get_bed_count(target_day):

    queryset = models.Riyosya.objects.filter(
        Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__gt=target_day)
        |
        Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__isnull=True)
        |
        Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte=settings.YAKIN_START_TIME)
        |
        Q(riyoukikans__start_day=(target_day+ timedelta(days=1)), riyoukikans__start_time__lt=settings.NIKKIN_START_TIME)
        |
        Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte=settings.YAKIN_START_TIME)
    )

    return queryset.count()


@register.filter(name='get_riyosya_max_count')
def get_riyosya_max_count(target_day):

    queryset_day = models.Riyosya.objects.filter(
        Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__gt=target_day)
        |
        Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__isnull=True)
        |
        Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte=settings.NIKKIN_START_TIME, riyoukikans__start_time__lt=settings.YAKIN_START_TIME)
        |
        Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte=settings.NIKKIN_START_TIME)
        |
        Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte='00:00:00', riyoukikans__start_time__lt=settings.NIKKIN_START_TIME, riyoukikans__last_day__isnull=True)
    )

    queryset_night = models.Riyosya.objects.filter(
        Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__gt=target_day)
        |
        Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__isnull=True)
        |
        Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte=settings.YAKIN_START_TIME)
        |
        Q(riyoukikans__start_day=(target_day+ timedelta(days=1)), riyoukikans__start_time__lt=settings.NIKKIN_START_TIME)
        |
        Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte=settings.YAKIN_START_TIME)
    )

    if queryset_day.count() >= queryset_night.count():
        riyosya_max_count = queryset_day.count()
    else:
        riyosya_max_count = queryset_night.count()

    return riyosya_max_count


@register.filter(name='get_nyutaisyo')
def get_nyutaisyo(target_day):
    rrs = models.RiyosyaRiyouKikan.objects.filter(
        Q(start_day=target_day)
        |
        Q(last_day=target_day)).annotate(
            nyu=Case(
                When(start_day=target_day,then=0),
                When(last_day=target_day,then=1), output_field=IntegerField()
                ),
            order_time=Case(
                When(start_day=target_day,then='start_time'),
                When(last_day=target_day,then='last_time'), output_field=TimeField()
            )).order_by('order_time')

    return rrs
