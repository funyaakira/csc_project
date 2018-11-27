from django import forms
from ..models import Riyosya, Kiroku, riyosya_status

class KirokuCreateForm(forms.ModelForm):
    class Meta():
        model = Kiroku
        fields = ['exec_date', 'day_night', 'riyosya', 'date', 'time', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control form-control-sm col-4', 'readonly':'readonly'}),
            'time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control form-control-sm col-12',
                       'row': 5,
                       'placeholder': '一般介護状況を入力してください。',}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['riyosya'].queryset = Riyosya.objects.filter(status=riyosya_status[0][0]).order_by('furigana')
