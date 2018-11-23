from django import forms
from ..models import Kiroku

class KirokuCreateForm(forms.ModelForm):
    class Meta():
        model = Renraku
        fields = ['date', 'staff', 'memo']

class RenrakuKojinCreateForm(forms.ModelForm):
    class Meta():
        model = Renraku_kojin
        fields = ['date', 'riyosya', 'staff', 'memo']
