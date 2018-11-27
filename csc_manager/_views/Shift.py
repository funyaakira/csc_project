from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import Calendar

from ..models import Shift, Staff


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

        # # イベントの取得、設定
        # kwargs['events'] = Event.objects.filter(date=self.target_day)

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
        kwargs["year"] = year
        kwargs["month"] = month
        kwargs["week_names"] = week_names
        kwargs["shifts_dic"] = shifts_dic

        today = date.today()
        kwargs["today"] = today

        target_month = date(year, month, 1)
        kwargs["prev_year"] = (target_month - relativedelta(months=1)).year
        kwargs["prev_month"] = (target_month - relativedelta(months=1)).month
        kwargs["next_year"] = (target_month + relativedelta(months=1)).year
        kwargs["next_month"] = (target_month + relativedelta(months=1)).month

        return super().get_context_data(**kwargs)
