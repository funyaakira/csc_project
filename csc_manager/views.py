from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse
from .models import Staff, Shift, Event

from datetime import datetime, timedelta, date
import logging

from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


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

        queryset = Shift.objects.filter(date=self.target_day).order_by('shift_knd__shift_disp_order')
        return queryset

@csrf_exempt
def receive_from_gas(request):

	logger = logging.getLogger('django')
	s_Cnt = int(float(request.POST['s_Cnt']))
	logger.info(u"data count: " + str(s_Cnt))
	s_Data = request.POST['s_Data']
	logger.info(u"data: " + s_Data)

	s_Data_List = s_Data.split(",")
	# logger.info(u"s_Data_List: " + str(s_Data_List))

	# とりあえず当月のデータを削除
	dateF = datetime.strptime(s_Data_List[0],"%Y-%m-%d")
	# logger.info(u"dateF: " + str(dateF))
	dateT = dateF+relativedelta(months=1)
	# logger.info(u"dateT: " + str(dateT))
	DT_SHIFT.objects.filter(SHIFT_DATE__gte=dateF,SHIFT_DATE__lt=dateT).delete()
	# logger.info(u"Data Deleteted")

	index = 0
	for i in range(s_Cnt):
		logger.info("loop: " + str(i))
		logger.info("index: " + str(index))
		logger.info("SHIFT_DATE = " + str(s_Data_List[index+ 0]))

		DT_SHIFT(
			SHIFT_DATE = s_Data_List[index+ 0],
			HAYABAN =   Staff.objects.get(id=int(s_Data_List[index+ 1])) if s_Data_List[index+ 1] else None,
			HAYABAN_E = Staff.objects.get(id=int(s_Data_List[index+ 2])) if s_Data_List[index+ 2] else None,
			NIKKIN  =   Staff.objects.get(id=int(s_Data_List[index+ 3])) if s_Data_List[index+ 3] else None,
			NIKKIN1 =   Staff.objects.get(id=int(s_Data_List[index+ 4])) if s_Data_List[index+ 4] else None,
			NIKKIN2 =   Staff.objects.get(id=int(s_Data_List[index+ 5])) if s_Data_List[index+ 5] else None,
			NIKKIN3 =   Staff.objects.get(id=int(s_Data_List[index+ 6])) if s_Data_List[index+ 6] else None,
			NIKKIN_E =  Staff.objects.get(id=int(s_Data_List[index+ 7])) if s_Data_List[index+ 7] else None,
			NIKKIN_E1 = Staff.objects.get(id=int(s_Data_List[index+ 8])) if s_Data_List[index+ 8] else None,
			NIKKIN_E2 = Staff.objects.get(id=int(s_Data_List[index+ 9])) if s_Data_List[index+ 9] else None,
			NIKKIN_E3 = Staff.objects.get(id=int(s_Data_List[index+10])) if s_Data_List[index+10] else None,
			OSOBAN =    Staff.objects.get(id=int(s_Data_List[index+11])) if s_Data_List[index+11] else None,
			OSOBAN_E =  Staff.objects.get(id=int(s_Data_List[index+12])) if s_Data_List[index+12] else None,
			YAKIN  =    Staff.objects.get(id=int(s_Data_List[index+13])) if s_Data_List[index+13] else None,
			AKE    =    Staff.objects.get(id=int(s_Data_List[index+14])) if s_Data_List[index+14] else None,
			KANGO1 =    Staff.objects.get(id=int(s_Data_List[index+15])) if s_Data_List[index+15] else None,
			KANGO2 =    Staff.objects.get(id=int(s_Data_List[index+16])) if s_Data_List[index+16] else None,
			SOUDANIN =  Staff.objects.get(id=int(s_Data_List[index+17])) if s_Data_List[index+17] else None,
			SEISOU =    Staff.objects.get(id=int(s_Data_List[index+18])) if s_Data_List[index+18] else None,
			MEMO     = s_Data_List[index+19]
		).save()
		index = index + 20

	return HttpResponse("通信成功")
