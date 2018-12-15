from django import forms

from django.db.models import Q

from ..models import Riyosya, RiyosyaRiyouKikan, start_kbn, last_kbn
from ..libs.funcs import wareki_to_seireki

class RiyosyaForm(forms.ModelForm):

    y_start_day = forms.DateField(
        required=False,
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'YYYY/MM/DD'},
        )
    )

    y_start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-2',
                   'placeholder': 'HH:MM'},
        )
    )

    y_start_kbn = forms.IntegerField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-4'},
            choices=start_kbn
        )
    )

    y_last_day = forms.DateField(
        required=False,
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3',
                   'placeholder': 'YYYY/MM/DD'},
        )
    )

    y_last_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-2',
                   'placeholder': 'HH:MM'},
        )
    )

    y_last_kbn = forms.IntegerField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-4'},
            choices=last_kbn
        )
    )

    gengou = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-2'},
            choices=((2, '大正'),(3, '昭和'),)
        )
    )

    g_year = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-2'},
            choices=[(i,i) for i in range(1, 64)]
        )
    )

    month = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-2'},
            choices=[(i,i) for i in range(1, 13)]
        )
    )

    day = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-2'},
            choices=[(i,i) for i in range(1, 32)]
        )
    )

    r_name_1 = forms.CharField(
        label='名前',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'})
    )

    r_furigana_1 = forms.CharField(
        label='ふりがな',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'})
    )

    r_zoku_1 = forms.CharField(
        label='続柄',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    r_addr_1 = forms.CharField(
        label='住所',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-8'})
    )

    r_tel_1_1 = forms.CharField(
        label='電話番号1',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    r_tel_2_1 = forms.CharField(
        label='電話番号2',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    r_name_2 = forms.CharField(
        label='名前',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'})
    )

    r_furigana_2 = forms.CharField(
        label='ふりがな',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'})
    )

    r_zoku_2 = forms.CharField(
        label='続柄',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    r_addr_2 = forms.CharField(
        label='住所',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-8'})
    )

    r_tel_1_2 = forms.CharField(
        label='電話番号1',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    r_tel_2_2 = forms.CharField(
        label='電話番号2',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-3'})
    )

    class Meta:
        model = Riyosya
        fields = ['name', 'furigana', 'sex', 'caremanager', 'addr', 'tel', 'youkaigodo', 'memo']
        widgets = {
            'first_day': forms.DateInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'furigana': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'sex': forms.Select(attrs={'class': 'form-control form-control-sm col-2'}),
            'caremanager': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'addr': forms.TextInput(attrs={'class': 'form-control form-control-sm col-12'}),
            'tel': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'youkaigodo': forms.Select(attrs={'class': 'form-control form-control-sm col-3'}),
            'memo': forms.Textarea(attrs={'row': 5,
                                          'placeholder': 'メモを入力してください',
                                          'class': 'form-control form-control-sm col-12'
                                         })
        }


    def clean(self):
        y_start_day = self.cleaned_data['y_start_day']
        y_last_day = self.cleaned_data['y_last_day']

        if y_start_day == y_last_day:
            self.add_error('y_start_day', '利用開始予定日と利用終了予定日が同日です。')
            self.add_error('y_last_day', '利用開始予定日と利用終了予定日が同日です。')

        if y_start_day is not None and y_last_day is not None:
            if y_start_day > y_last_day:
                self.add_error('y_start_day', '利用開始予定日と利用終了予定日が逆転しています。')
                self.add_error('y_last_day', '利用開始予定日と利用終了予定日が逆転しています。')

        gengou = self.cleaned_data['gengou']
        g_year = self.cleaned_data['g_year']
        month = self.cleaned_data['month']
        day = self.cleaned_data['day']

        d = wareki_to_seireki(gengou, g_year, month, day)
        if d is None:
            self.add_error('gengou', '誕生日の入力に誤りがあります。')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RiyosyaStartInput(forms.ModelForm):

    class Meta:
        model = RiyosyaRiyouKikan

        fields = ['start_day', 'start_time', 'start_kbn']

        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-3'}),
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
        }

    start_day = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3'},
        )
    )


class RiyosyaLastInput(forms.ModelForm):

    class Meta:
        model = RiyosyaRiyouKikan

        fields = ['last_day', 'last_time', 'last_kbn']

        widgets = {
            'last_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-3'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
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


class RiyosyaEditRiyoukikan(forms.ModelForm):

    class Meta:
        model = RiyosyaRiyouKikan

        fields = ['start_day', 'start_time', 'start_kbn',
            'last_day', 'last_time', 'last_kbn',]

        widgets = {
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
        }

    start_day = forms.DateField(
        input_formats=['%Y/%m/%d'],
        required=True,
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
        input_formats=['%Y/%m/%d'],
        required=False,
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
        self.id = kwargs.pop('id')
        super(RiyosyaEditRiyoukikan, self).__init__(*args, **kwargs)

    def clean(self):

        c_data = self.cleaned_data

        start_day = c_data['start_day'] if 'start_day' in c_data else None
        start_time = c_data['start_time'] if 'start_time' in c_data else None
        last_day = c_data['last_day'] if 'last_day' in c_data else None
        last_time = c_data['last_time'] if 'last_time' in c_data else None
        riyosya = self.riyosya
        id = self.id

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
                Q(~Q(id=id),riyosya=riyosya,start_day__lte=last_day,last_day__gte=last_day)
                |
                Q(~Q(id=id),riyosya=riyosya,start_day__lte=last_day,last_day__isnull=True)
                )

            if rrs:
                self.add_error('last_day', '利用終了予定日が他の利用期間と重複しています。')
                for rr in rrs:
                    j_start_day = rr.start_day if rr.start_day is not None else ''
                    j_last_day = rr.last_day if rr.last_day is not None else ''

                    self.add_error('last_day', '重複する利用期間：%s～%s' % (j_start_day, j_last_day))
