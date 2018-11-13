from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse
from .models import Staff, Shift, Event, Shift_knd

from datetime import datetime, timedelta, date
import logging

from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

from django.utils import timezone

@login_required
def home(request):
    year = date.today().year
    month = date.today().month
    day = date.today().day
    return redirect('shift_day', year=year, month=month, day=day)


@method_decorator(login_required, name='dispatch')
class ShiftView(ListView):
    model = Shift
    context_object_name = 'shifts'
    template_name = 'csc_manager/shift.html'

    def get_context_data(self, **kwargs):
        # 前の日と次の日の設定
        prev_day = self.target_day + timedelta(days=-1)
        kwargs['prev_day'] = prev_day

        next_day = self.target_day + timedelta(days=1)
        kwargs['next_day'] = next_day

        # イベントの取得、設定
        kwargs['events'] = Event.objects.filter(date=self.target_day)

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        self.target_day = date(year, month, day)

        queryset = Shift.objects.filter(
            date=self.target_day).order_by('shift_knd__shift_disp_order')
        return queryset

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

            Shift(date=date, shift_knd=shift_knd, staff=staff).save()

    return HttpResponse(str(date) + ' - ' + str(staff.id) + ' - ' + str(shift_knd.id))

class TestView(TemplateView):
    template_name = 'csc_manager/test.html'
