from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings

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
        kwargs['target_day'] = target_day
        kwargs['day_night_now'] = day_night_now

        if day_night_now == day_night[0][0]:
            kwargs['day_night_name'] = day_night[0][1]

            kwargs['prev_day'] = (target_day - timedelta(days=1))
            kwargs['prev_day_night'] = day_night[1][0]

            kwargs['next_day'] = target_day
            kwargs['next_day_night'] = day_night[1][0]

        elif day_night_now == day_night[1][0]:
            kwargs['day_night_name'] = day_night[1][1]

            kwargs['prev_day'] = target_day
            kwargs['prev_day_night'] = day_night[0][0]

            kwargs['next_day'] = (target_day + timedelta(days=1))
            kwargs['next_day_night'] = day_night[0][0]

        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=target_day, day_night=day_night_now).order_by('date', 'time')

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        target_day = date(year, month, day)
        yokujitu = target_day + timedelta(days=1)

        if self.kwargs.get('day_night') == day_night[0][0]:
            queryset = Riyosya.objects.filter(
                Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__gt=target_day)
                |
                Q(riyoukikans__start_day__lt=target_day, riyoukikans__last_day__isnull=True)
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte=settings.NIKKIN_START_TIME, riyoukikans__start_time__lt=settings.YAKIN_START_TIME)
                |
                Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte=settings.NIKKIN_START_TIME)
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte='00:00:00', riyoukikans__start_time__lt=settings.NIKKIN_START_TIME, riyoukikans__last_day__isnull=True)
            ).order_by('furigana')
        elif self.kwargs.get('day_night') == day_night[1][0]:
            queryset = Riyosya.objects.filter(
                Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__gt=target_day)
                |
                Q(riyoukikans__start_day__lte=target_day, riyoukikans__last_day__isnull=True)
                |
                Q(riyoukikans__start_day=target_day, riyoukikans__start_time__gte=settings.YAKIN_START_TIME)
                |
                Q(riyoukikans__start_day=yokujitu, riyoukikans__start_time__lt=settings.NIKKIN_START_TIME)
                |
                Q(riyoukikans__last_day=target_day, riyoukikans__last_time__gte=settings.YAKIN_START_TIME)
            ).order_by('furigana')

        # 連続投入用に利用者IDのリストを作ってsessionに格納しておく
        riyosya_order_list = []
        for r in queryset:
            riyosya_order_list.append(r.id)

        self.request.session['riyosya_order_list'] = riyosya_order_list

        return queryset


class KirokuCreateView(CreateView):
    model = Kiroku
    context_object_name = 'kiroku'
    form_class = KirokuCreateForm
    template_name = 'csc_manager/kiroku_create.html'
