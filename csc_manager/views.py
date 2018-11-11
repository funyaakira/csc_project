from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse
from .models import StaffInfo, Shift, Event

from datetime import datetime, timedelta, date
import logging

from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


@login_required
def home(request):
    today_obj = Shift.objects.get(date=date.today())
    return redirect('shift_day', pk=today_obj.pk)

@method_decorator(login_required, name='dispatch')
class ShiftView(DetailView):
    model = Shift
    context_object_name = 'shift'
    template_name = 'csc_manager/shift.html'

    def get_context_data(self, **kwargs):
        # 前の日と次の日の設定
        pk = self.kwargs.get('pk')
        target_day = Shift.objects.get(pk=pk).date

        prev_day = target_day + timedelta(days=-1)
        next_day = target_day + timedelta(days=1)
        kwargs['prev_day_pk'] = Shift.objects.get(date=prev_day).pk
        kwargs['next_day_pk'] = Shift.objects.get(date=next_day).pk

        # イベントの取得、設定
        kwargs['events'] = Event.objects.filter(date=target_day)

        return super().get_context_data(**kwargs)


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
			HAYABAN =   StaffInfo.objects.get(id=int(s_Data_List[index+ 1])) if s_Data_List[index+ 1] else None,
			HAYABAN_E = StaffInfo.objects.get(id=int(s_Data_List[index+ 2])) if s_Data_List[index+ 2] else None,
			NIKKIN  =   StaffInfo.objects.get(id=int(s_Data_List[index+ 3])) if s_Data_List[index+ 3] else None,
			NIKKIN1 =   StaffInfo.objects.get(id=int(s_Data_List[index+ 4])) if s_Data_List[index+ 4] else None,
			NIKKIN2 =   StaffInfo.objects.get(id=int(s_Data_List[index+ 5])) if s_Data_List[index+ 5] else None,
			NIKKIN3 =   StaffInfo.objects.get(id=int(s_Data_List[index+ 6])) if s_Data_List[index+ 6] else None,
			NIKKIN_E =  StaffInfo.objects.get(id=int(s_Data_List[index+ 7])) if s_Data_List[index+ 7] else None,
			NIKKIN_E1 = StaffInfo.objects.get(id=int(s_Data_List[index+ 8])) if s_Data_List[index+ 8] else None,
			NIKKIN_E2 = StaffInfo.objects.get(id=int(s_Data_List[index+ 9])) if s_Data_List[index+ 9] else None,
			NIKKIN_E3 = StaffInfo.objects.get(id=int(s_Data_List[index+10])) if s_Data_List[index+10] else None,
			OSOBAN =    StaffInfo.objects.get(id=int(s_Data_List[index+11])) if s_Data_List[index+11] else None,
			OSOBAN_E =  StaffInfo.objects.get(id=int(s_Data_List[index+12])) if s_Data_List[index+12] else None,
			YAKIN  =    StaffInfo.objects.get(id=int(s_Data_List[index+13])) if s_Data_List[index+13] else None,
			AKE    =    StaffInfo.objects.get(id=int(s_Data_List[index+14])) if s_Data_List[index+14] else None,
			KANGO1 =    StaffInfo.objects.get(id=int(s_Data_List[index+15])) if s_Data_List[index+15] else None,
			KANGO2 =    StaffInfo.objects.get(id=int(s_Data_List[index+16])) if s_Data_List[index+16] else None,
			SOUDANIN =  StaffInfo.objects.get(id=int(s_Data_List[index+17])) if s_Data_List[index+17] else None,
			SEISOU =    StaffInfo.objects.get(id=int(s_Data_List[index+18])) if s_Data_List[index+18] else None,
			MEMO     = s_Data_List[index+19]
		).save()
		index = index + 20

	return HttpResponse("通信成功")
