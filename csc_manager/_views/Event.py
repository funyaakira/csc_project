from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from ..models import Event
from .._forms.Event import EventForm


# イベント - 一覧
class EventListView(TemplateView):
    template_name = 'csc_manager/event_list.html'

    def get_context_data(self, **kwargs):

        # 指定年月の取得
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        # 年月指定がない場合は当月を設定
        if year == None:
            now = datetime.now()
            year = now.year
            month = now.month

        # カレンダーの機能を利用して、指定年月のdateオブジェクトのリストを作成
        days = [date(year, month, i+1)
            for i in range(calendar.monthrange(year, month)[1])]

        # 指定月の条件でイベントオブジェクトを取得
        dateF = date(year, month, 1)
        dateT = dateF + relativedelta(months=1)
        events = Event.objects.filter(date__gte=dateF, date__lt=dateT)

        # テンプレートに渡す
        kwargs["days"] = days
        kwargs["events"] = events

        return super().get_context_data(**kwargs)


# イベント - 新規
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'csc_manager/event_create.html'

    def form_valid(self, form):
        print('form_valid')
        form.save()
        # post = form.save(commit=False)
        # post.created_by = self.request.user
        # post.created_at = timezone.now()
        # post.updated_by = self.request.user
        # post.updated_at = timezone.now()
        #
        # # birthday設定
        # gengou = self.request.POST['gengou']
        # g_year = self.request.POST['g_year']
        # month = self.request.POST['month']
        # day = self.request.POST['day']
        # post.birthday = wareki_to_seireki(gengou, g_year, month, day)
        #
        # post.save()
        #
        return redirect('event_list')
