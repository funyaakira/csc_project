from django import forms
from .models import Riyosya, gender, Test
import bootstrap_datepicker_plus as datetimepicker
from datetime import date
from .libs.funcs import wareki_to_seireki


class TestForm(forms.ModelForm):
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

    class Meta:
        model = Test
        fields = ('name', 'sex', 'birthday')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'sex': forms.Select(attrs={'class': 'form-control col-2'}),
            # 'birthday': DateOfBirthWidget(order='MDY', attrs={'class': 'form-control'}),
        }
