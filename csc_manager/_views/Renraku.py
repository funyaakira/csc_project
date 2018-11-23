from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import date

from ..models import Renraku, Renraku_kojin
from .._forms.Renraku import RenrakuCreateForm, RenrakuKojinCreateForm


class RenrakuListView(ListView):
    model = Renraku
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_list.html'

    def get_queryset(self):
        queryset = Renraku.objects.all().order_by('-date')

        return queryset


class RenrakuCreateView(CreateView):
    model = Renraku
    form_class = RenrakuCreateForm
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_create.html'

    def get_initial(self):
        return {
            'staff': self.request.user.staff,
            'date': date.today()
        }

    def form_valid(self, form):
        form.save()

        return redirect('renraku_list')


class RenrakuKojinListView(ListView):
    model = Renraku_kojin
    context_object_name = 'renraku_kojins'
    template_name = 'csc_manager/renraku_kojin_list.html'

    def get_queryset(self):
        queryset = Renraku_kojin.objects.all().order_by('-date')

        return queryset


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
