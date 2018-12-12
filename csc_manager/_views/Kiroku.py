from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from ..models import Riyosya, Kiroku, day_night, riyosya_status, Staff
from .._forms.Kiroku import *
import codecs


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

        kwargs['target_day'] = target_day
        kwargs['prev_day_1week'] = target_day - timedelta(days=7)
        kwargs['day_night'] = day_night_now
        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=target_day, day_night=day_night_now).order_by('date', 'disp_time')
        kwargs['riyosya_ids'] = self.riyosya_ids # get_querysetで設定した利用者IDをカンマ区切りで連結したもの

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

        ## 連続投入用に利用者IDのリストを作ってsessionに格納しておく
        # riyosya_order_list = []
        # for r in queryset:
        #     riyosya_order_list.append(r.id)
        #
        # self.request.session['riyosya_order_list'] = riyosya_order_list

        # 連続投入用に利用者IDをカンマでつなげた文字列作成
        l_riyosya_ids = []
        for r in queryset:
            l_riyosya_ids.append(str(r.id))
        self.riyosya_ids = ','.join(l_riyosya_ids)

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

        riyosya_ids = self.kwargs.get('riyosya_ids').split(',')
        riyosya_id_current_index = self.kwargs.get('riyosya_id_current_index')
        riyosya_id = riyosya_ids[riyosya_id_current_index]

        l_day_night = self.kwargs.get('day_night')

        return {
            'exec_date': date(year, month, day),
            'day_night': l_day_night,
            'riyosya': riyosya_id,
            'date': date(year, month, day),
            # 'time': datetime.now().strftime("%H:%M"),
            'time': None,
            'staff': self.request.user.staff.name,
        }

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        l_day_night = self.kwargs.get('day_night')
        exec_date = date(year, month, day)

        riyosya_ids = self.kwargs.get('riyosya_ids')
        riyosya_ids_list = riyosya_ids.split(',')
        riyosya_id_current_index = int(self.kwargs.get('riyosya_id_current_index'))
        riyosya_id = riyosya_ids_list[riyosya_id_current_index]
        riyosya = Riyosya.objects.get(id=riyosya_id)

        riyosya_id_prev_index = riyosya_id_current_index - 1
        riyosya_id_current_index += 1
        kwargs['riyosya_id_current_index'] = riyosya_id_current_index
        kwargs['riyosya_id_prev_index'] = riyosya_id_prev_index
        kwargs['riyosya_id_curent_index_back_use'] = riyosya_id_current_index - 1

        if len(riyosya_ids_list) == riyosya_id_current_index:
            kwargs['last_riyosya'] = True
            riyosya_id = riyosya_ids_list[riyosya_id_prev_index]
            kwargs['prev_riyosya'] = Riyosya.objects.get(id=riyosya_id)
        else:
            kwargs['last_riyosya'] = False
            if riyosya_id_current_index == 1:
                kwargs['first_riyosya'] = True
                riyosya_id = riyosya_ids_list[riyosya_id_current_index]
                kwargs['next_riyosya'] = Riyosya.objects.get(id=riyosya_id)
            else:
                riyosya_id = riyosya_ids_list[riyosya_id_current_index]
                kwargs['next_riyosya'] = Riyosya.objects.get(id=riyosya_id)
                riyosya_id = riyosya_ids_list[riyosya_id_prev_index]
                kwargs['prev_riyosya'] = Riyosya.objects.get(id=riyosya_id)


        kwargs['riyosya'] = riyosya
        kwargs['riyosya_ids'] = riyosya_ids
        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=exec_date, riyosya=riyosya).order_by('date', 'disp_time', '-time')
        kwargs['target_day'] = exec_date
        kwargs['year'] = year
        kwargs['month'] = month
        kwargs['day'] = day
        kwargs['target_day'] = exec_date
        kwargs['day_night'] = l_day_night
        kwargs['day_night_name'] = day_night[l_day_night][1]

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        kiroku = form.save(commit=False)

        kiroku.disp_time = kiroku.time

        if kiroku.time == None:
            if kiroku.day_night == settings._NIKKIN:
                kiroku.disp_time = '12:00'
            else:
                kiroku.disp_time = '00:00'

        if kiroku.day_night == settings._YAKIN:
            if kiroku.time == None:
                in_time = time(0, 0, 0)
            else:
                in_time = kiroku.time

            if time(0, 0, 0) <= in_time < settings.NIKKIN_START_TIME:
                kiroku.date += timedelta(days=1)

        kiroku.created_by = self.request.user
        kiroku.created_at = timezone.now()
        kiroku.updated_by = self.request.user
        kiroku.updated_at = timezone.now()

        kiroku.save()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')
        riyosya_ids = self.kwargs.get('riyosya_ids')
        riyosya_ids_list = riyosya_ids.split(',')
        riyosya_id_current_index = int(self.kwargs.get('riyosya_id_current_index'))

        if 'commit_next' in self.request.POST:
            riyosya_id_current_index += 1

        if len(riyosya_ids_list) == riyosya_id_current_index:
            return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)
        else:
            return redirect('kiroku_create',
             year=year, month=month, day=day, day_night=day_night, riyosya_ids=riyosya_ids,
             riyosya_id_current_index=riyosya_id_current_index)


# class KirokuEditView(UpdateView):
#     model = Kiroku
#     context_object_name = 'kiroku'
#     form_class = KirokuEditForm
#     template_name = 'csc_manager/kiroku/edit.html'

    # def get_initial(self):
    #     year = self.kwargs.get('year')
    #     month = self.kwargs.get('month')
    #     day = self.kwargs.get('day')
    #
    #     riyosya_ids = self.kwargs.get('riyosya_ids').split(',')
    #     riyosya_id_current_index = self.kwargs.get('riyosya_id_current_index')
    #     riyosya_id = riyosya_ids[riyosya_id_current_index]
    #
    #     l_day_night = self.kwargs.get('day_night')
    #
    #     return {
    #         'exec_date': date(year, month, day),
    #         'day_night': l_day_night,
    #         'riyosya': riyosya_id,
    #         'date': date(year, month, day),
    #         # 'time': datetime.now().strftime("%H:%M"),
    #         'time': None,
    #         'staff': self.request.user.staff.name,
    #     }

    # def get_context_data(self, **kwargs):
    #
    #     kwargs['return_url'] = self.kwargs.get('return_url')
    #     kwargs['scroll_position'] = self.kwargs.get('scroll_position')
    #
    #     return super().get_context_data(**kwargs)

    # def form_valid(self, form):
    #     kiroku = form.save(commit=False)
    #
    #     kiroku.disp_time = kiroku.time
    #
    #     if kiroku.time == None:
    #         if kiroku.day_night == settings._NIKKIN:
    #             kiroku.disp_time = '12:00'
    #         else:
    #             kiroku.disp_time = '00:00'
    #
    #     if kiroku.day_night == settings._YAKIN:
    #         if kiroku.time == None:
    #             in_time = time(0, 0, 0)
    #         else:
    #             in_time = kiroku.time
    #
    #         if time(0, 0, 0) <= in_time < settings.NIKKIN_START_TIME:
    #             kiroku.date += timedelta(days=1)
    #
    #     kiroku.created_by = self.request.user
    #     kiroku.created_at = timezone.now()
    #     kiroku.updated_by = self.request.user
    #     kiroku.updated_at = timezone.now()
    #
    #     kiroku.save()
    #
    #     year = self.kwargs.get('year')
    #     month = self.kwargs.get('month')
    #     day = self.kwargs.get('day')
    #     day_night = self.kwargs.get('day_night')
    #     riyosya_ids = self.kwargs.get('riyosya_ids')
    #     riyosya_ids_list = riyosya_ids.split(',')
    #     riyosya_id_current_index = int(self.kwargs.get('riyosya_id_current_index'))
    #
    #     if 'commit_next' in self.request.POST:
    #         riyosya_id_current_index += 1
    #
    #     if len(riyosya_ids_list) == riyosya_id_current_index:
    #         return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)
    #     else:
    #         return redirect('kiroku_create',
    #          year=year, month=month, day=day, day_night=day_night, riyosya_ids=riyosya_ids,
    #          riyosya_id_current_index=riyosya_id_current_index)


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


class KirokuKojinListView(ListView):
    model = Kiroku
    context_object_name = 'kirokus'
    template_name = 'csc_manager/kiroku/kojin.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        riyosya_id = self.kwargs.get('riyosya_id')
        target_YM = date(year, month, 1)

        kwargs['target_YM'] = target_YM
        kwargs['riyosya'] = Riyosya.objects.get(id=riyosya_id)
        kwargs['prev_month'] = target_YM - relativedelta(months=1)
        kwargs['next_month'] = target_YM + relativedelta(months=1)

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        riyosya_id = self.kwargs.get('riyosya_id')
        riyosya = Riyosya.objects.get(id=riyosya_id)

        target_YM = date(year, month, 1)
        next_YM = target_YM + relativedelta(months=1)

        queryset = Kiroku.objects.filter(
            riyosya=riyosya,
            exec_date__gte=target_YM,
            exec_date__lt=next_YM).order_by('date', 'disp_time')

        return queryset


def kiroku_delete(request, year, month, day, day_night, riyosya_ids, riyosya_id_current_index, pk):

    Kiroku.objects.get(id=pk).delete()

    if riyosya_ids == 'list':
        return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night)

    return redirect('kiroku_create', year=year, month=month, day=day, day_night=day_night, riyosya_ids=riyosya_ids, riyosya_id_current_index=riyosya_id_current_index)


def kiroku_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filepath = settings.MEDIA_ROOT + '/' + filename
        import_kiroku(filepath)
        uploaded_file_url = fs.url(filename)
        return render(request, 'csc_manager/kiroku/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'csc_manager/kiroku/upload.html')


def import_kiroku(filepath):

    # ケース記録データインポート
    f =  codecs.open(filepath, 'r', 'utf-8')
    line = f.readline()

    while line:
        data_l = line.split("\t")
        print(data_l)

        riyosya_name = data_l[0]
        k_date = data_l[1]
        k_time = data_l[2]
        memo = data_l[3]
        staff_name = data_l[4].strip()

        riyosya = Riyosya.objects.get(name=riyosya_name)
        staff = Staff.objects.get(short_name=staff_name)

        # 特殊時間の設定
        if k_time == 'x':
            k_time = None
            disp_time = time(12, 0, 0)
        elif k_time == 'z':
            k_time = None
            disp_time = time(0, 0, 0)
        else:
            dt = datetime.strptime(k_time, '%H:%M')
            k_time = time(hour=dt.hour, minute=dt.minute)
            disp_time = k_time

        dt = datetime.strptime(k_date, '%Y-%m-%d')
        k_date = date(year=dt.year, month=dt.month, day=dt.day)

        print(k_date, k_time, disp_time)
        line = f.readline()

        # exec_dateの設定
        if time(0, 0, 0) <= disp_time < settings.NIKKIN_START_TIME:
            exec_date = k_date - timedelta(days=1)
        else:
            exec_date = k_date

        # day_nightの設定
        if settings.NIKKIN_START_TIME <= disp_time < settings.YAKIN_START_TIME:
            day_night = settings._NIKKIN
        else:
            day_night = settings._YAKIN

        # オブジェクトを組み立てて更新
        Kiroku(exec_date=exec_date,
               date=k_date,
               time=k_time,
               disp_time=disp_time,
               day_night=day_night,
               riyosya=riyosya,
               memo=memo,
               created_by=staff.user).save()

    f.close()

    return None
