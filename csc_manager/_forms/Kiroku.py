from django import forms
from ..models import Riyosya, Kiroku, riyosya_status

class KirokuCreateForm(forms.ModelForm):
    class Meta():
        model = Kiroku
        fields = ['exec_date', 'date', 'time', 'memo', 'day_night', 'riyosya', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['riyosya'].queryset = Riyosya.objects.filter(status=riyosya_status[0][0]).order_by('furigana')
