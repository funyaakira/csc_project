from django import forms

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
            'start_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-2'}),
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
            'last_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-2'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-4'}),
        }

    start_day = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3'},
        )
    )

    last_day = forms.DateField(
        required=False,
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-sm col-3'},
        )
    )
