from django import forms
from ..models import Renraku

class RenrakuCreateForm(forms.ModelForm):
    class Meta():
        model = Renraku
        fields = ['date', 'staff', 'memo']
        
