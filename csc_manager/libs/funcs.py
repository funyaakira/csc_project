from datetime import datetime, date


def seireki_to_wareki(arg):

    if arg == None:
        return ''

    syouwaGannen = date(1926, 12, 25)
    heiseiGnanen = date(1989, 1, 8)

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
    else:
        gengo = "平成"
        year -= 1988

    wareki = gengo + str(year) + '年' + str(month) + '月' + str(day) + '日'

    return wareki


def wareki_to_seireki(gengou, g_year, month, day):

    year = 0
    if gengou == '2':
        year = int(g_year) + 1911
    elif gengou == '3':
        year = int(g_year) + 1925

    return date(year, int(month), int(day))


def calculate_age(born):
    """年齢を返す"""
    today = date.today()  # 今日

    age = today.year - born.year

    # 今年の誕生日を迎えていなければ、ageを1つ減らす
    # 今日を表すタプル(7, 29) < 誕生日を表すタプル(7, 30)
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age
