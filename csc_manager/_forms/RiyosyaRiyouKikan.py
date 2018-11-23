from django import forms

from ..models import RiyosyaRiyouKikan


class RiyosyaRiyouKikanForm(forms.ModelForm):
    class Meta:
        model = RiyosyaRiyouKikan
        fields = ['last_day',
                  'last_kbn',
                  'memo',]
        widgets = {
            'last_day': forms.DateInput(attrs={'class': 'form-control form-control-sm col-5'}),
            'last_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-5'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control form-control-sm col-12',
                       'row': 5,
                       'placeholder': '特別な退所理由がある場合は入力してください',}),
        }


class RiyosyaRiyouKikanForm_Renew(forms.ModelForm):
    class Meta:
        model = RiyosyaRiyouKikan
        fields = ['riyosya',
                  'start_day',
                  'start_kbn',]
        widgets = {
            'start_day': forms.DateInput(attrs={'class': 'form-control form-control-sm col-3'}),
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-3'}),
        }
