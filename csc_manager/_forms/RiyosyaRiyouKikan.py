from django import forms
from django.db.models import Q

from ..models import RiyosyaRiyouKikan


class RiyosyaRiyouKikanForm(forms.ModelForm):
    class Meta:
        model = RiyosyaRiyouKikan
        fields = ['last_day',
                  'last_time',
                  'last_kbn',
                  'memo',]
        widgets = {
            'last_day': forms.DateInput(attrs={'class': 'form-control form-control-sm col-3'}),
            'last_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-3'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control form-control-sm col-10',
                       'rows': 5,
                       'placeholder': '特別な退所理由がある場合は入力してください',}),
        }

    last_day = forms.DateField(
        input_formats=['%Y/%m/%d'],
        required=True,
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'YYYY/MM/DD'},
        )
    )
    last_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'HH:MM'},
        )
    )

class RiyosyaRiyouKikanForm_Renew(forms.ModelForm):

    class Meta:
        model = RiyosyaRiyouKikan

        fields = ['riyosya', 'start_day', 'start_time','start_kbn',
                  'last_day', 'last_time', 'last_kbn',]

        widgets = {
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
        }

    start_day = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'YYYY/MM/DD'},
        )
    )

    start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'HH:MM'},
        )
    )

    last_day = forms.DateField(
        required=False,
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'YYYY/MM/DD'},
        )
    )

    last_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'HH:MM'},
        )
    )

    def __init__(self, *args, **kwargs):
        self.riyosya = kwargs.pop('riyosya')
        super(RiyosyaRiyouKikanForm_Renew, self).__init__(*args, **kwargs)

    def clean(self):

        c_data = self.cleaned_data

        start_day = c_data['start_day'] if 'start_day' in c_data else None
        start_time = c_data['start_time'] if 'start_time' in c_data else None
        last_day = c_data['last_day'] if 'last_day' in c_data else None
        last_time = c_data['last_time'] if 'last_time' in c_data else None
        riyosya = self.riyosya

        if start_day and last_day:
            if start_day == last_day:
                self.add_error('start_day', '利用開始予定日と利用終了予定日が同日です。')
                self.add_error('last_day', '利用開始予定日と利用終了予定日が同日です。')

        if start_day is not None and last_day is not None:
            if start_day > last_day:
                self.add_error('start_day', '利用開始予定日と利用終了予定日が逆転しています。')
                self.add_error('last_day', '利用開始予定日と利用終了予定日が逆転しています。')

        if last_day is None and last_time is not None:
            self.add_error('last_day', '利用終了予定時間のみの入力はできません。')


        if last_day is not None:
            rrs = RiyosyaRiyouKikan.objects.filter(
                Q(riyosya=riyosya,start_day__lte=last_day,last_day__gte=last_day)
                |
                Q(riyosya=riyosya,start_day__lte=last_day,last_day__isnull=True)
                )

            if rrs:
                self.add_error('last_day', '利用終了予定日が他の利用期間と重複しています。')
                for rr in rrs:
                    j_start_day = rr.start_day if rr.start_day is not None else ''
                    j_last_day = rr.last_day if rr.last_day is not None else ''

                    self.add_error('last_day', '重複する利用期間：%s～%s' % (j_start_day, j_last_day))

        if start_day is not None:
            rrs = RiyosyaRiyouKikan.objects.filter(
                Q(riyosya=riyosya,start_day__lte=start_day,last_day__gte=start_day)
                |
                Q(riyosya=riyosya,start_day__lte=start_day,last_day__isnull=True)
                )

            if rrs:
                self.add_error('start_day', '利用開始予定日が他の利用期間と重複しています。')
                for rr in rrs:
                    j_start_day = rr.start_day if rr.start_day is not None else ''
                    j_last_day = rr.last_day if rr.last_day is not None else ''

                    self.add_error('start_day', '重複する利用期間：%s～%s' % (j_start_day, j_last_day))
