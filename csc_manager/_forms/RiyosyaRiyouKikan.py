from django import forms

from ..models import RiyosyaRiyouKikan

class RiyosyaRiyouKikanForm(forms.ModelForm):
    class Meta:
        model = RiyosyaRiyouKikan
        fields = '__all__'
