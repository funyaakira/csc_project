from django import forms
from .models import Riyosya, gender, Test

class RiyosyaNewForm(forms.ModelForm):
    class Meta:
        model = Riyosya
        fields = ['first_day', 'name', 'furigana', 'sex', 'birthday', 'caremanager']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name=="村山明":
            raise forms.ValidationError('氏名に村山明は使用できません')

        return name
