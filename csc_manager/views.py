from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, CreateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from django.urls import reverse
from calendar import Calendar

from .models import Staff, Shift, Event, Shift_knd, Riyosya, Test
from .forms import RiyosyaForm, TestForm

@login_required
def home(request):
    year = date.today().year
    month = date.today().month
    day = date.today().day
    return redirect('shift_day', year=year, month=month, day=day)


# シフト単日表示
@method_decorator(login_required, name='dispatch')
class ShiftDayView(ListView):
    model = Shift
    context_object_name = 'shifts'
    template_name = 'csc_manager/shift_day.html'

    def get_context_data(self, **kwargs):
        kwargs['target_day'] = self.target_day

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


# シフト個人カレンダー表示
@method_decorator(login_required, name='dispatch')
class ShiftIndivView(TemplateView):
    template_name = 'csc_manager/shift_indiv.html'

    def get_context_data(self, **kwargs):
        # スタッフオブジェクトの取得・設定
        pk = self.kwargs.get('pk')
        staff = Staff.objects.get(pk=pk)

        # カレンダー情報の取得・設定
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        days = Calendar(firstweekday=6).monthdatescalendar(year, month)
        week_names = ['日','月','火','水','木','金','土',]

        # スタッフ、当月の条件でシフトオブジェクトを取得・設定
        dateF = date(year, month, 1)
        dateT = dateF + relativedelta(months=1)
        shifts = Shift.objects.filter(staff=staff, date__gte=dateF, date__lt=dateT).order_by("date")

        ## テンプレートで参照できるように辞書に格納し直す
        ## キーは "日"
        shifts_dic = {}
        for shift in shifts:
            shifts_dic[shift.date.day] = shift

        # テンプレートに渡す
        kwargs["staff"] = staff
        kwargs["days"] = days
        kwargs["month"] = month
        kwargs["week_names"] = week_names
        kwargs["shifts_dic"] = shifts_dic
        kwargs["today"] = date.today()

        return super().get_context_data(**kwargs)


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


# 利用者 - トップ(一覧)
class RiyosyaListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/riyosyas.html'

    def get_queryset(self):
        queryset = Riyosya.objects.filter(
            taisyo_flg=False
        ).order_by('furigana')

        return queryset


# 利用者 - 新規入所
class RiyosyaNewView(CreateView):
    model = Riyosya
    form_class = RiyosyaForm
    template_name = 'csc_manager/riyosya_new.html'
    success_url = "riyosya_list"

    def form_valid(self, form):
        try:
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.created_at = timezone.now()
            post.updated_by = self.request.user
            post.updated_at = timezone.now()
            post.save()
        except:
            pass

        return redirect('riyosya_list')


class TestView(TemplateView):
    template_name = 'csc_manager/test.html'

class TestCreateView(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'test.html'
    success_url = '/'
