from django import forms

from ..models import Riyosya, start_kbn
from ..libs.funcs import wareki_to_seireki


class RiyosyaForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'class': 'form-control form-control-sm col-2'},
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

    start_kbn = forms.IntegerField(
        label='入所時間区分',
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-3'},
            choices=start_kbn
        )
    )

    class Meta:
        model = Riyosya
        fields = ['first_day', 'name', 'furigana', 'sex', 'caremanager', 'addr', 'tel', 'youkaigodo', 'memo']
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


    def clean_name(self):
        name = self.cleaned_data['name']

        if name=="村山明":
            self.fields["name"].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('氏名に村山明は使用できません')

        return name


    def clean(self):
        try:
            gengou = self.cleaned_data['gengou']
            g_year = self.cleaned_data['g_year']
            month = self.cleaned_data['month']
            day = self.cleaned_data['day']

            d = wareki_to_seireki(gengou, g_year, month, day)
        except:
            # raise forms.ValidationError('誕生日がおかしいです')
            pass


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
