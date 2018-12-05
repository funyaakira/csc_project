from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from django.urls import reverse

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from ..models import Event, Event_knd, Staff
from .._forms.Event import EventForm


# イベント - 一覧
class EventListView(TemplateView):
    template_name = 'csc_manager/event/list.html'

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
        events = Event.objects.filter(date__gte=dateF, date__lt=dateT).order_by('time')

        # テンプレートに渡す
        kwargs["year"] = year
        kwargs["month"] = month
        kwargs["days"] = days
        kwargs["events"] = events
        kwargs['target_YM'] = date(year, month, 1)
        kwargs['prev_YM'] = date(year, month, 1) - relativedelta(months=1)
        kwargs['next_YM'] = date(year, month, 1) + relativedelta(months=1)

        return super().get_context_data(**kwargs)


# イベント - 新規
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'csc_manager/event/create.html'

    def get_initial(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        return {
            'date': date(year, month, day),
            # 'time': datetime.now().strftime("%H:%M"),
            'knd': self.kwargs.get('event_knd_id'),
        }

    def get_form_kwargs(self):
        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs['event_knd_id'] = self.kwargs.get('event_knd_id')
        return kwargs

    def get_context_data(self, **kwargs):
        # 指定年月の取得
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        scroll_position = self.kwargs.get('scroll_position')

        kwargs["event_knds"] = Event_knd.objects.all().order_by('id')
        kwargs['event_knd_id'] = self.kwargs.get('event_knd_id')

        kwargs["date"] = date(year, month, day)
        kwargs["year"] = year
        kwargs["month"] = month
        kwargs["day"] = day
        kwargs["scroll_position"] = scroll_position

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        scroll_position = self.kwargs.get('scroll_position')

        event = form.save(commit=False)

        event.save()

        return redirect('event_list_with_scroll_postion', year=year, month=month, scroll_position=scroll_position)


# イベント - 削除
def eventDelete(request, year, month, day, event_id, scroll_position):

    Event.objects.get(id=event_id).delete()

    return redirect('event_list_with_scroll_postion', year=year, month=month, scroll_position=scroll_position)
