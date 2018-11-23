from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import datetime, date

from ..models import Riyosya, Kiroku, day_night, riyosya_status


@login_required
def kiroku_home(request):

    year = date.today().year
    month = date.today().month
    day = date.today().day
    hour = datetime.now().hour
    if hour >= 0 and hour < 9:
        day -= 1

    return redirect('kiroku_day_list', year=year, month=month, day=day, day_night=day_night[0][0])


class KirokuDayListView(ListView):
    model = Riyosya
    context_object_name = 'riyosyas'
    template_name = 'csc_manager/kiroku_day_list.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        day_night = self.kwargs.get('day_night')

        target_day = date(year, month, day)
        kwargs['target_day'] = date(year, month, day)
        kwargs['kirokus'] = Kiroku.objects.filter(exec_date=target_day, day_night=day_night).order_by('date', 'time')

        return super().get_context_data(**kwargs)

    def get_queryset(self):

        queryset = Riyosya.objects.filter(
            status=riyosya_status[0][0],
        ).order_by('furigana')

        return queryset
