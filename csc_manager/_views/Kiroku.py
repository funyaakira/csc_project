from django.views.generic import ListView, CreateView, DeleteView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
from django.urls import reverse

from datetime import datetime, date, timedelta

from ..models import Riyosya, Kiroku, day_night, riyosya_status
from .._forms.Kiroku import *


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
    template_name = 'csc_manager/kiroku/day_list.html'

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

        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=target_day, day_night=day_night_now).order_by('date', 'disp_time')

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
    template_name = 'csc_manager/kiroku/create.html'

    def get_initial(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        riyosya_id = self.kwargs.get('riyosya_id')
        l_day_night = self.kwargs.get('day_night')

        # 夜勤の場合はデフォルトの日付を翌日に設定
        if l_day_night == day_night[0][0]:
            def_date = date(year, month, day)
            def_time = '12:00'
        else:
            def_date = date(year, month, day) + timedelta(days=1)
            def_time = '00:00'

        return {
            'exec_date': date(year, month, day),
            'day_night': l_day_night,
            'riyosya': riyosya_id,
            'date': def_date,
            'time': def_time,
            'staff': self.request.user.staff.name,
        }

    def get_context_data(self, **kwargs):
        year= self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')
        exec_date = date(year, month, day)

        riyosya_id = self.kwargs.get('riyosya_id')
        riyosya = Riyosya.objects.get(id=riyosya_id)

        kwargs['riyosya'] = riyosya
        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=exec_date, riyosya=riyosya).order_by('date', 'disp_time')
        kwargs['year'] = year
        kwargs['month'] = month
        kwargs['day'] = day
        kwargs['day_night'] = day_night

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        kiroku = form.save(commit=False)

        kiroku.disp_time = kiroku.time

        if kiroku.time == None:
            if kiroku.day_night == settings._NIKKIN:
                kiroku.disp_time = '12:00'
            else:
                kiroku.disp_time = '00:00'

        kiroku.created_by = self.request.user
        kiroku.created_at = timezone.now()
        kiroku.updated_by = self.request.user
        kiroku.updated_at = timezone.now()

        riyosya = kiroku.riyosya
        kiroku.save()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')

        if 'commit_list' in self.request.POST:
            return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)
        else:
            return redirect('kiroku_create', year=year, month=month, day=day, day_night=day_night, riyosya_id=riyosya.id)

class KirokuRenzokuCreateView(CreateView):
    model = Kiroku
    context_object_name = 'kiroku'
    form_class = KirokuCreateForm
    template_name = 'csc_manager/kiroku/renzoku_create.html'

    def get_initial(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        riyosya_order_list_idx = self.kwargs.get('riyosya_order_list_idx')
        riyosya_order_list = self.request.session['riyosya_order_list']
        riyosya_id = riyosya_order_list[riyosya_order_list_idx]

        l_day_night = self.kwargs.get('day_night')

        # 夜勤の場合はデフォルトの日付を翌日に設定
        if l_day_night == day_night[0][0]:
            def_date = date(year, month, day)
            def_time = None
        else:
            def_date = date(year, month, day) + timedelta(days=1)
            def_time = None

        return {
            'exec_date': date(year, month, day),
            'day_night': l_day_night,
            'riyosya': riyosya_id,
            'date': def_date,
            # 'time': datetime.now().strftime("%H:%M"),
            'time': None,
            'staff': self.request.user.staff.name,
        }

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        exec_date = date(year, month, day)
        kwargs['target_day'] = exec_date

        kwargs['day_night'] = self.kwargs.get('day_night')

        riyosya_order_list_idx = self.kwargs.get('riyosya_order_list_idx')
        riyosya_order_list = self.request.session['riyosya_order_list']
        riyosya_id = riyosya_order_list[riyosya_order_list_idx]
        riyosya = Riyosya.objects.get(id=riyosya_id)
        kwargs['riyosya'] = riyosya

        riyosya_order_list_idx += 1
        if len(riyosya_order_list) == riyosya_order_list_idx:
            kwargs['go_to_back'] = True
        else:
            kwargs['riyosya_order_list_idx'] = riyosya_order_list_idx
            riyosya_id = riyosya_order_list[riyosya_order_list_idx]
            kwargs['next_riyosya'] = Riyosya.objects.get(id=riyosya_id)

        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=exec_date, riyosya=riyosya).order_by('date', 'disp_time')

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        kiroku = form.save(commit=False)

        kiroku.disp_time = kiroku.time

        if kiroku.time == None:
            if kiroku.day_night == settings._NIKKIN:
                kiroku.disp_time = '12:00'
            else:
                kiroku.disp_time = '00:00'

        kiroku.created_by = self.request.user
        kiroku.created_at = timezone.now()
        kiroku.updated_by = self.request.user
        kiroku.updated_at = timezone.now()

        kiroku.save()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')

        riyosya_order_list = self.request.session['riyosya_order_list']
        riyosya_order_list_idx = self.kwargs.get('riyosya_order_list_idx')

        if 'commit_next' in self.request.POST:
            riyosya_order_list_idx += 1

        if len(riyosya_order_list) == riyosya_order_list_idx:
            return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)
        else:
            return redirect('kiroku_renzoku_create', year=year, month=month, day=day, day_night=day_night, riyosya_order_list_idx=riyosya_order_list_idx)


class KirokuDeleteView(DeleteView):
    model = Kiroku
    context_object_name = 'kiroku'
    form_class = KirokuDeleteForm
    template_name = 'csc_manager/kiroku/delete.html'
    success_url = "/"

    def get_success_url(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')

        return reverse('kiroku_day_list',  kwargs={'year': year, 'month': month, 'day': day, 'day_night': day_night})
        # return reverse('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)
