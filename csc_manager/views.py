from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from datetime import date

from .models import Shift, Shift_knd


@login_required
def home(request):
    year = date.today().year
    month = date.today().month
    day = date.today().day
    return redirect('shift_day', year=year, month=month, day=day)


# GoogleSpreadSheetのシフトデータを受け取る
@csrf_exempt
def receive_from_gas(request):

    shift_data = request.POST['shift_data']
    shift_data_ary = shift_data.split('\r\n')

    # とりあえず当月のデータを削除
    dateF = shift_data_ary[0].split(",")[0]
    dateF = datetime.strptime(dateF, '%Y/%m/%d')
    dateT = dateF + relativedelta(months=1)
    Shift.objects.filter(date__gte=dateF, date__lt=dateT).delete()

    for shift_data in shift_data_ary:
        date = shift_data.split(",")[0]
        date = timezone.datetime.strptime(date, '%Y/%m/%d')
        name = shift_data.split(",")[1]
        short_name = shift_data.split(",")[2]

        if short_name != '':
            staff = Staff.objects.get(name=name)
            shift_knd = Shift_knd.objects.get(short_name=short_name)

            # 固定シフトが登録されている場合は、それを登録(休み以外)
            if shift_knd.catergory != '休':
                if staff.fixed_shift != None:
                    shift_knd = staff.fixed_shift

            Shift(date=date, shift_knd=shift_knd, staff=staff).save()

    return HttpResponse('正常終了しました')


# class TestView(TemplateView):
#     template_name = 'csc_manager/test.html'
#
# class TestCreateView(CreateView):
#     model = Test
#     form_class = TestForm
#     template_name = 'test.html'
#     success_url = '/'
