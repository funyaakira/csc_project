from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q

from datetime import datetime, date, timedelta

from ..models import Riyosya, Kiroku, day_night, riyosya_status
from .._forms.Kiroku import KirokuCreateForm


@login_required
def kiroku_home(request):

    year = date.today().year
    month = date.today().month
    day = date.today().day
    hour = datetime.now().hour
    if hour >= 0 and hour < 9:
        day -= 1

    if hour >= 18 or hour < 9:
        now_day_night = day_night[1]
    else:
        now_day_night = day_night[0]

    return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=now_day_night[0])


class KirokuDayListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/kiroku_day_list.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night_now = self.kwargs.get('day_night')

        target_day = date(year, month, day)
        kwargs['target_day'] = date(year, month, day)
        kwargs['day_night_now'] = day_night_now

        if day_night_now == day_night[0][0]:
            day_night_name = day_night[0][1]
        elif day_night_now == day_night[1][0]:
            day_night_name = day_night[1][1]
        kwargs['day_night_name'] = day_night_name

        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=target_day, day_night=day_night_now).order_by('date', 'time')

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        target_day = date(year, month, day)
        yokujitu = target_day + timedelta(days=1)
        # queryset = Riyosya.objects.filter(
        #     status=riyosya_status[0][0],
        # ).order_by('furigana')

        if self.kwargs.get('day_night') == day_night[0][0]:
            queryset = Riyosya.objects.filter(
                Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__gt=target_day)
                |
                Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__isnull=True)
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte='09:00:00', riyoukikans__start_time__lt='18:00:00')
                |
                Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte='09:00:00', riyoukikans__start_time__lt='18:00:00')
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte='00:00:00', riyoukikans__start_time__lt='9:00:00', riyoukikans__last_day__isnull=True)
            ).order_by('furigana')
        elif self.kwargs.get('day_night') == day_night[1][0]:
            queryset = Riyosya.objects.filter(
                Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__gt=target_day)
                |
                Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__isnull=True)
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte='18:00:00')
                |
                Q(riyoukikans__start_day=yokujitu, riyoukikans__start_time__lt='09:00:00')
                |
                Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte='18:00:00')
            ).order_by('furigana')
        return queryset


class KirokuCreateView(CreateView):
    model = Kiroku
    context_object_name = 'kiroku'
    form_class = KirokuCreateForm
    template_name = 'csc_manager/kiroku_create.html'
