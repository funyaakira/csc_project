from django.views.generic import ListView, CreateView
from django.utils import timezone
from django.shortcuts import redirect
from django.db import transaction

from ..models import Riyosya, RiyosyaRiyouKikan, RiyosyaRenrakusaki
from .._forms.Riyosya import RiyosyaForm
from ..libs.funcs import wareki_to_seireki


# 利用者 - トップ(一覧)
class RiyosyaListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/riyosyas.html'

    def get_queryset(self):
        queryset = Riyosya.objects.filter(
            taisyo_flg=False,
        ).order_by('furigana')

        return queryset


# 利用者 - 新規入所
class RiyosyaNewView(CreateView):
    model = Riyosya
    form_class = RiyosyaForm
    template_name = 'csc_manager/riyosya_new.html'
    success_url = "riyosya_list"

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

        # RiyosyaRiyouKikan 更新
        RiyosyaRiyouKikan(
            riyosya=post,
            start_day=post.first_day,
            last_day=None,
            created_by=self.request.user,
            created_at=timezone.now(),
            updated_by=self.request.user,
            updated_at=timezone.now()
        ).save()

        # RiyosyaRenrakusaki 更新
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
