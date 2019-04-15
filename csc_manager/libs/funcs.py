from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from ..models import Riyosya, RiyosyaRiyouKikan

from django.conf import settings
from django.db.models import Q

def seireki_to_wareki(arg):

    if arg == None:
        return ''

    syouwaGannen = date(1926, 12, 25)
    heiseiGnanen = date(1989, 1, 8)
    reiwaGannen = date(2019, 5, 1)

    year = arg.year
    month = arg.month
    day = arg.day

    gengo = ''
    if arg < syouwaGannen:
        gengo = '大正'
        year -= 1911
    elif syouwaGannen <= arg < heiseiGnanen:
        gengo = "昭和"
        year -= 1925
    elif heiseiGnanen <= arg < reiwaGannen:
        gengo = "平成"
        year -= 1988
    else:
        gengo = "令和"
        year -= 2018

    wareki = gengo + str(year) + '年' + str(month) + '月' + str(day) + '日'

    return wareki


def wareki_to_seireki(gengou, g_year, month, day):

    try:
        year = 0
        if int(gengou) == 2:
            year = int(g_year) + 1911
        elif int(gengou) == 3:
            print('xxxx')
            syouwa_err = False
            if int(g_year) == 1:
                if int(month) == 12:
                    if int(day) < 25:
                        syouwa_err = True
                else:
                    syouwa_err = True

            if not syouwa_err:
                year = int(g_year) + 1925

        returnDate = date(year, int(month), int(day))
    except:
        returnDate = None

    return returnDate


def calculate_age(born):
    """年齢を返す"""
    today = date.today()  # 今日

    age = today.year - born.year

    # 今年の誕生日を迎えていなければ、ageを1つ減らす
    # 今日を表すタプル(7, 29) < 誕生日を表すタプル(7, 30)
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age


def get_riyosyas_target_month(year, month):
    # 指定の年月を利用した利用者のリストを取得

    target_day_from = date(year, month, 1)
    target_day_to = target_day_from + relativedelta(months=1)

    rs = Riyosya.objects.filter(
        Q(riyoukikans__start_day__lte=target_day_from, riyoukikans__last_day__isnull=True)
        |
        Q(riyoukikans__start_day__lte=target_day_from, riyoukikans__last_day__lte=target_day_to, riyoukikans__last_day__gte=target_day_from)
        |
        Q(riyoukikans__start_day__gte=target_day_from, riyoukikans__last_day__lte=target_day_to)
        |
        Q(riyoukikans__start_day__gte=target_day_from, riyoukikans__last_day__isnull=True)
    ).order_by('furigana').distinct()

    return rs


def exist_riyosya(riyosya, day):
    # 指定の日付に指定の利用者が利用しているか判定
    rs = RiyosyaRiyouKikan.objects.filter(
        Q(riyosya=riyosya, start_day__lte=day, last_day__isnull=True)
        |
        Q(riyosya=riyosya, start_day__lte=day, last_day__gte=day)
    )

    return rs
