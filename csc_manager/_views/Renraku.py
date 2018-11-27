from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import date

from ..models import Renraku, Renraku_kojin, Riyosya
from .._forms.Renraku import RenrakuCreateForm, RenrakuKojinCreateForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class RenrakuZentaiListView(ListView):
    model = Renraku
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_zentai_list.html'

    def get_queryset(self):
        queryset = Renraku.objects.all().order_by('-date', '-id')

        return queryset


@method_decorator(login_required, name='dispatch')
class RenrakuZentaiDetailView(DetailView):
    model = Renraku
    context_object_name = 'renraku'
    template_name = 'csc_manager/renraku_zentai_detail.html'


@method_decorator(login_required, name='dispatch')
class RenrakuZentaiCreateView(CreateView):
    model = Renraku
    form_class = RenrakuCreateForm
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_zentai_create.html'

    def get_initial(self):
        return {
            'staff': self.request.user.staff,
            'date': date.today()
        }

    def form_valid(self, form):
        form.save()

        return redirect('renraku_list')


@method_decorator(login_required, name='dispatch')
class RenrakuKojinListView(ListView):
    model = Renraku_kojin
    context_object_name = 'renraku_kojins'
    template_name = 'csc_manager/renraku_kojin_list.html'

    def get_queryset(self):
        queryset = Renraku_kojin.objects.all().order_by('-date', '-id')

        return queryset


@method_decorator(login_required, name='dispatch')
class RenrakuKojinListRiyosyaView(ListView):
    model = Renraku_kojin
    context_object_name = 'renraku_kojins'
    template_name = 'csc_manager/renraku_kojin_list_riyosya.html'

    def get_context_data(self, **kwargs):
        riyosya_id = self.kwargs.get('riyosya_pk')
        riyosya = Riyosya.objects.get(id=riyosya_id)
        kwargs['riyosya'] = riyosya
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        riyosya_id = self.kwargs.get('riyosya_pk')
        riyosya = Riyosya.objects.get(id=riyosya_id)
        queryset = Renraku_kojin.objects.filter(riyosya=riyosya).order_by('-date')

        return queryset


@method_decorator(login_required, name='dispatch')
class RenrakuKojinDetailView(DetailView):
    model = Renraku_kojin
    context_object_name = 'renraku_kojin'
    template_name = 'csc_manager/renraku_kojin_detail.html'


@method_decorator(login_required, name='dispatch')
class RenrakuKojinCreateView(CreateView):
    model = Renraku_kojin
    form_class = RenrakuKojinCreateForm
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_kojin_create.html'

    def get_initial(self):
        return {
            'staff': self.request.user.staff,
            'date': date.today()
        }

    def form_valid(self, form):
        form.save()

        return redirect('renraku_kojin_list')
