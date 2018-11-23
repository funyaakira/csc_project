from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import date

from ..models import Renraku
from .._forms.Renraku import RenrakuCreateForm


class RenrakuListView(ListView):
    model = Renraku
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_list.html'


class RenrakuCreateView(CreateView):
    model = Renraku
    form_class = RenrakuCreateForm
    context_object_name = 'renrakus'
    template_name = 'csc_manager/renraku_create.html'

    def get_initial(self):
        return {
            'staff': self.request.user,
            'date': date.today()
        }

    def form_valid(self, form):
        form.save()

        return redirect('renraku_list')
