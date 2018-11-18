from django import forms
from .models import Riyosya, gender, Test
import bootstrap_datepicker_plus as datetimepicker
from datetime import date
from .libs.funcs import wareki_to_seireki

class RiyosyaForm(forms.ModelForm):
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
        model = Riyosya
        fields = ['first_day', 'start_kbn', 'name', 'furigana', 'sex', 'caremanager', 'addr', 'tel', 'youkaigodo']
        widgets = {
            # 'first_day': datetimepicker.DatePickerInput(
            #     format='%Y-%m-%d',
            #     options={
            #         'locale': 'ja',
            #         'dayViewHeaderFormat': 'YYYY年 MMMM',
            #     }
            # ),
            'first_day': forms.DateInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'start_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'furigana': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'sex': forms.Select(attrs={'class': 'form-control form-control-sm col-2'}),
            'caremanager': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'addr': forms.TextInput(attrs={'class': 'form-control form-control-sm col-12'}),
            'tel': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'youkaigodo': forms.Select(attrs={'class': 'form-control form-control-sm col-3'}),
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

        self.name = forms.CharField(max_length=10,
                        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm col-4 is-valid'}))
        self.name.label_classes = ('form-control-sm', )
        # self.name.label = '氏名'
        # print(self.name.label)
        # print(dir(self.name.label))
        # for field in self.fields.values():
        #     # my_class = field.widget.attrs['class']
        #     field.widget.attrs['class'] = 'form-control'




















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
