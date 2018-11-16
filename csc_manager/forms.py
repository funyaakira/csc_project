from django import forms
from .models import Riyosya, gender, Test
from dobwidget import DateOfBirthWidget

class RiyosyaForm(forms.ModelForm):
    class Meta:
        model = Riyosya
        fields = ['first_day', 'name', 'furigana', 'sex', 'birthday', 'caremanager']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name=="村山明":
            raise forms.ValidationError('氏名に村山明は使用できません')

        return name

class TestForm(forms.ModelForm):
    gengou = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm col-2'},
            choices=(('大正', '大正'),('昭和', '昭和'),)
        )
    )

    class Meta:
        model = Test
        fields = ('name', 'sex', 'birthday')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'sex': forms.Select(attrs={'class': 'form-control col-2'}),
            'birthday': DateOfBirthWidget(order='MDY', attrs={'class': 'form-control'}),
        }
