from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse
from .models import DT_SHIFT, MT_STAFF, DT_SHIFT, DT_EVENT

from datetime import datetime,timedelta,date
import logging

from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required


def index(request):
	output = get_output(request, date.today())
	return HttpResponse(output)



def shift_day(request, shift_day):
	d_targetday = datetime.strptime(shift_day, '%Y-%m-%d')
	output = get_output(request, d_targetday)
	return HttpResponse(output)



def get_output(request, target_day):

	shift_data = DT_SHIFT.objects.get(SHIFT_DATE=target_day)
	event_data_list = DT_EVENT.objects.filter(EV_DATE=target_day)

	output = target_day

	if shift_data:
		prev_day = target_day + timedelta(days=-1)
		next_day = target_day + timedelta(days=1)

		template = loader.get_template('csc_manager/index.html')
		context = {
			'shift_data': shift_data,
			'event_data_list': event_data_list,
			'today': date.today(),
			'prev_day': prev_day,
			'next_day': next_day
		}
		output = template.render(context, request)

	return output

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
			HAYABAN =   MT_STAFF.objects.get(id=int(s_Data_List[index+ 1])) if s_Data_List[index+ 1] else None,
			HAYABAN_E = MT_STAFF.objects.get(id=int(s_Data_List[index+ 2])) if s_Data_List[index+ 2] else None,
			NIKKIN  =   MT_STAFF.objects.get(id=int(s_Data_List[index+ 3])) if s_Data_List[index+ 3] else None,
			NIKKIN1 =   MT_STAFF.objects.get(id=int(s_Data_List[index+ 4])) if s_Data_List[index+ 4] else None,
			NIKKIN2 =   MT_STAFF.objects.get(id=int(s_Data_List[index+ 5])) if s_Data_List[index+ 5] else None,
			NIKKIN3 =   MT_STAFF.objects.get(id=int(s_Data_List[index+ 6])) if s_Data_List[index+ 6] else None,
			NIKKIN_E =  MT_STAFF.objects.get(id=int(s_Data_List[index+ 7])) if s_Data_List[index+ 7] else None,
			NIKKIN_E1 = MT_STAFF.objects.get(id=int(s_Data_List[index+ 8])) if s_Data_List[index+ 8] else None,
			NIKKIN_E2 = MT_STAFF.objects.get(id=int(s_Data_List[index+ 9])) if s_Data_List[index+ 9] else None,
			NIKKIN_E3 = MT_STAFF.objects.get(id=int(s_Data_List[index+10])) if s_Data_List[index+10] else None,
			OSOBAN =    MT_STAFF.objects.get(id=int(s_Data_List[index+11])) if s_Data_List[index+11] else None,
			OSOBAN_E =  MT_STAFF.objects.get(id=int(s_Data_List[index+12])) if s_Data_List[index+12] else None,
			YAKIN  =    MT_STAFF.objects.get(id=int(s_Data_List[index+13])) if s_Data_List[index+13] else None,
			AKE    =    MT_STAFF.objects.get(id=int(s_Data_List[index+14])) if s_Data_List[index+14] else None,
			KANGO1 =    MT_STAFF.objects.get(id=int(s_Data_List[index+15])) if s_Data_List[index+15] else None,
			KANGO2 =    MT_STAFF.objects.get(id=int(s_Data_List[index+16])) if s_Data_List[index+16] else None,
			SOUDANIN =  MT_STAFF.objects.get(id=int(s_Data_List[index+17])) if s_Data_List[index+17] else None,
			SEISOU =    MT_STAFF.objects.get(id=int(s_Data_List[index+18])) if s_Data_List[index+18] else None,
			MEMO     = s_Data_List[index+19]
		).save()
		index = index + 20

	return HttpResponse("通信成功")
