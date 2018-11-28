from django.views.generic import ListView, CreateView, UpdateView
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, date, timedelta

from ..models import Riyosya, RiyosyaRiyouKikan, RiyosyaRenrakusaki, gender, riyosya_status
from .._forms.Riyosya import RiyosyaForm
from .._forms.RiyosyaRiyouKikan import RiyosyaRiyouKikanForm, RiyosyaRiyouKikanForm_Renew
from ..libs.funcs import wareki_to_seireki



# 利用者 - トップ(一覧)
@method_decorator(login_required, name='dispatch')
class RiyosyaListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/riyosya/list.html'

    def get_context_data(self, **kwargs):
        kwargs['riyosya_count'] = Riyosya.objects.filter(
                status=riyosya_status[0][0]).count

        kwargs['riyosya_man_count'] = Riyosya.objects.filter(
                status=riyosya_status[0][0],
                sex=gender[0][0]).count

        kwargs['riyosya_woman_count'] = Riyosya.objects.filter(
                status=riyosya_status[0][0],
                sex=gender[1][0]).count

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Riyosya.objects.filter(
            status=riyosya_status[0][0],
        ).order_by('furigana')

        return queryset


# 利用者 - 新規入所
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

        post = form.save(commit=False)
        post.created_by = self.request.user
        post.created_at = timezone.now()
        post.updated_by = self.request.user
        post.updated_at = timezone.now()

        # birthday設定
        gengou = self.request.POST['gengou']
        g_year = self.request.POST['g_year']
        month = self.request.POST['month']
        day = self.request.POST['day']
        post.birthday = wareki_to_seireki(gengou, g_year, month, day)
        post.save()

        # RiyosyaRiyouKikan 作成
        RiyosyaRiyouKikan(
            riyosya=post,
            start_day=post.first_day,
            start_time=self.request.POST['start_time'],
            start_kbn= self.request.POST['start_kbn'],
            last_day=None,
            last_time=None,
            last_kbn=None,
            created_by=self.request.user,
            created_at=timezone.now(),
            updated_by=self.request.user,
            updated_at=timezone.now()
        ).save()

        # RiyosyaRenrakusaki 作成
        RiyosyaRenrakusaki(
            riyosya=post,
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

    def get_queryset(self):
        queryset = Riyosya.objects.filter(
            status=riyosya_status[1][0],
        ).order_by('-last_day')

        return queryset


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
        post.created_by = self.request.user
        post.created_at = timezone.now()
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        # Riyosya status 更新
        r = Riyosya.objects.get(id=post.riyosya.id)
        r.status = riyosya_status[0][0]
        r.last_day = None
        r.updated_by = self.request.user
        r.updated_at = timezone.now()
        r.save()

        return redirect('riyosya_list')
