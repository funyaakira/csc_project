from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db import models
from django.db.models import Q
from django.db.models.functions import Concat

from datetime import datetime, date, timedelta

from ..models import Riyosya, RiyosyaRiyouKikan, RiyosyaRenrakusaki, gender, riyosya_status
from .._forms.Riyosya import RiyosyaForm, RiyosyaStartInput, RiyosyaLastInput
from .._forms.RiyosyaRiyouKikan import RiyosyaRiyouKikanForm, RiyosyaRiyouKikanForm_Renew
from ..libs.funcs import wareki_to_seireki



# 利用者 - トップ(一覧)
@method_decorator(login_required, name='dispatch')
class RiyosyaListView(ListView):
    model = RiyosyaRiyouKikan
    context_object_name = 'riyosya_riyoukians'
    template_name = 'csc_manager/riyosya/list.html'

    def get_context_data(self, **kwargs):
        kwargs['target_day'] = self.target_day

        kwargs['riyosya_count'] = self.nyusyo.count

        kwargs['riyosya_man_count'] = self.nyusyo_man.count

        kwargs['riyosya_woman_count'] = self.nyusyo_woman.count

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if year:
            self.target_day = date(year, month, day)
        else:
            self.target_day = date.today()

        queryset = (
            RiyosyaRiyouKikan.objects.filter(
                Q(start_day__lte=self.target_day, last_day__isnull=True)
                |
                Q(start_day__lte=self.target_day, last_day__gte=self.target_day, last_status=settings._TAISYO_YOTEI)
            ).order_by('riyosya__furigana')
        )

        self.nyusyo = queryset.filter(start_status=0)
        self.nyusyo_man = self.nyusyo.filter(riyosya__sex=1)
        self.nyusyo_woman = self.nyusyo.filter(riyosya__sex=2)

        return queryset



# 利用者 - 実利用開始日時確定
class RiyosyaStartInputView(UpdateView):
    model = RiyosyaRiyouKikan
    form_class = RiyosyaStartInput
    context_object_name = 'rr'
    template_name = 'csc_manager/riyosya/start_input.html'

    def get_success_url(self):
        return reverse('riyosya_list')

    def get_initial(self):
        start_day = self.object.start_day
        start_day = "{}/{}/{}".format(start_day.year, start_day.month, start_day.day)

        if self.object.start_time:
            start_time = self.object.start_time
            start_time = "{0}:{1:02d}".format(start_time.hour, start_time.minute)
        else:
            start_time = None

        return {'start_day': start_day, 'start_time': start_time }

    def form_valid(self, form):
        rr = form.save(commit=False)
        rr.start_status = settings._RIYOSYA_STATUS_NYUSYO
        rr.save()

        riyosya = Riyosya.objects.get(id=rr.riyosya.id)
        riyosya.status = settings._RIYOSYA_STATUS_NYUSYO

        if riyosya.first_day is None:
            riyosya.first_day = rr.start_day

        riyosya.save()

        return redirect('riyosya_list')



# 利用者 - 実利用終了日時確定
class RiyosyaLastInputView(UpdateView):
    model = RiyosyaRiyouKikan
    form_class = RiyosyaLastInput
    context_object_name = 'rr'
    template_name = 'csc_manager/riyosya/last_input.html'

    def get_success_url(self):
        return reverse('riyosya_list')

    def get_initial(self):
        last_day = self.object.last_day
        last_day = "{}/{}/{}".format(last_day.year, last_day.month, last_day.day)
        last_time = self.object.last_time
        last_time = "{0}:{1:02d}".format(last_time.hour, last_time.minute)

        return {'last_day': last_day, 'last_time': last_time }

    def form_valid(self, form):
        rr = form.save(commit=False)
        rr.last_status = settings._TAISYO_KAKUTEI
        rr.save()

        riyosya = Riyosya.objects.get(id=rr.riyosya.id)
        riyosya.status = settings._RIYOSYA_STATUS_TAISYO
        riyosya.last_day = rr.last_day
        riyosya.save()

        return redirect('riyosya_list')



# 利用者 - 詳細
class RiyosyaDetailView(DetailView):
    model = Riyosya
    template_name = 'csc_manager/riyosya/detail.html'



# 利用者 - 新規利用予定
class RiyosyaNewView(CreateView):
    model = Riyosya
    form_class = RiyosyaForm
    template_name = 'csc_manager/riyosya/new.html'
    success_url = "riyosya_list"

    def get_initial(self):
        return {
            'first_day': date.today(),
            'start_time': datetime.now().strftime("%H:%M"),
        }

    def form_valid(self, form):

        riyosya = form.save(commit=False)
        riyosya.status = settings._RIYOSYA_STATUS_YOTEI
        riyosya.created_by = self.request.user
        riyosya.created_at = timezone.now()
        riyosya.updated_by = self.request.user
        riyosya.updated_at = timezone.now()

        # birthday設定
        gengou = self.request.POST['gengou']
        g_year = self.request.POST['g_year']
        month = self.request.POST['month']
        day = self.request.POST['day']
        riyosya.birthday = wareki_to_seireki(gengou, g_year, month, day)
        riyosya.save()

        # RiyosyaRiyouKikan 作成 (予定として登録)
        RiyosyaRiyouKikan(
            riyosya=riyosya,
            start_day=self.request.POST['y_start_day'] if self.request.POST['y_start_day'] !='' else None,
            start_time=self.request.POST['y_start_time'] if self.request.POST['y_start_time'] !='' else None,
            start_kbn=self.request.POST['y_start_kbn'],
            start_status=settings._RIYOSYA_STATUS_YOTEI,
            last_day=self.request.POST['y_last_day'] if self.request.POST['y_last_day'] !='' else None,
            last_time=self.request.POST['y_last_time'] if self.request.POST['y_last_time'] !='' else None,
            last_kbn=self.request.POST['y_last_kbn'],
            last_status=settings._RIYOSYA_STATUS_YOTEI,
            created_by=self.request.user,
            created_at=timezone.now(),
            updated_by=self.request.user,
            updated_at=timezone.now()
        ).save()

        # RiyosyaRenrakusaki 作成
        RiyosyaRenrakusaki(
            riyosya=riyosya,
            name=self.request.POST['r_name_1'],
            furigana=self.request.POST['r_furigana_1'],
            zokugara=self.request.POST['r_zoku_1'],
            addr=self.request.POST['r_addr_1'],
            tel=self.request.POST['r_tel_1_1'],
            tel2=self.request.POST['r_tel_2_1'],
            primary_flg=True,
            created_by=self.request.user,
            created_at=timezone.now(),
            updated_by=self.request.user,
            updated_at=timezone.now()
        ).save()

        if self.request.POST['r_name_2']:
            RiyosyaRenrakusaki(
                riyosya=post,
                name=self.request.POST['r_name_2'],
                furigana=self.request.POST['r_furigana_2'],
                zokugara=self.request.POST['r_zoku_2'],
                addr=self.request.POST['r_addr_2'],
                tel=self.request.POST['r_tel_1_2'],
                tel2=self.request.POST['r_tel_2_2'],
                primary_flg=False,
                created_by=self.request.user,
                created_at=timezone.now(),
                updated_by=self.request.user,
                updated_at=timezone.now()
            ).save()

        return redirect('riyosya_list')



# 利用者 - 利用予定者一覧
class RiyosyaYoteiListView(ListView):
    model = RiyosyaRiyouKikan
    context_object_name = 'riyosya_riyoukians'
    template_name = 'csc_manager/riyosya/yotei_list.html'

    def get_context_data(self, **kwargs):
        kwargs['target_day'] = self.target_day
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if year:
            self.target_day = date(year, month, day)
        else:
            self.target_day = date.today()

        queryset = (
            RiyosyaRiyouKikan.objects.filter(
                start_day__gt=self.target_day
            ).order_by('start_day')
        )
        print(queryset.query)
        return queryset



# 利用者 - 退所
class RiyosyaTaisyoView(UpdateView):
    model = RiyosyaRiyouKikan
    form_class = RiyosyaRiyouKikanForm
    template_name = 'csc_manager/riyosya/taisyo.html'
    success_url = "riyosya_list"

    def get_initial(self):
        return {
            'last_day': date.today(),
            'last_time': datetime.now().strftime("%H:%M"),
        }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.last_status = settings._TAISYO_KAKUTEI
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        # Riyosya status 更新
        r = Riyosya.objects.get(id=post.riyosya.id)
        r.status = riyosya_status[1][0]
        r.last_day = post.last_day
        r.save()

        return redirect('riyosya_list')



# 退所者 - 退所者一覧
class TaisyoListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/riyosya/taisyo/list.html'

    def get_context_data(self, **kwargs):
        kwargs['target_day'] = self.target_day
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if year:
            self.target_day = date(year, month, day)
        else:
            self.target_day = date.today()

        queryset = Riyosya.objects.filter(
            status=riyosya_status[1][0],
        ).order_by('-last_day')

        return queryset



# 退所者 - 詳細
class TaisyoDetailView(DetailView):
    model = Riyosya
    template_name = 'csc_manager/riyosya/taisyo/detail.html'



# 退所者 - 再入所
class TaisyoRenewView(CreateView):
    model = RiyosyaRiyouKikan
    form_class = RiyosyaRiyouKikanForm_Renew
    template_name = 'csc_manager/riyosya/taisyo/renew.html'
    success_url = "riyosya_list"

    def get_initial(self):
        return {
            'riyosya':self.kwargs.get('pk'),
        }

    def get_context_data(self, **kwargs):
        kwargs['riyosya'] = Riyosya.objects.get(id=self.kwargs.get('pk'))

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.start_status = settings._RIYOSYA_STATUS_YOTEI
        post.last_status = settings._RIYOSYA_STATUS_YOTEI
        post.created_by = self.request.user
        post.created_at = timezone.now()
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        # Riyosya status 更新
        r = Riyosya.objects.get(id=post.riyosya.id)
        r.status = settings._RIYOSYA_STATUS_YOTEI
        r.last_day = None
        r.updated_by = self.request.user
        r.updated_at = timezone.now()
        r.save()

        return redirect('riyosya_list')
