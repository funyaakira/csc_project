from django import forms
from django.conf import settings

from datetime import datetime, timedelta

from ..models import Riyosya, Kiroku, riyosya_status

class KirokuCreateForm(forms.ModelForm):
    staff = forms.CharField(
        label='記録者',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-4', 'readonly':'readonly'},
        )
    )

    class Meta():
        model = Kiroku
        fields = ['exec_date', 'day_night', 'riyosya', 'date', 'time', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control col-4'}),
            'time': forms.TimeInput(attrs={'class': 'form-control col-4'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control col-12',
                       'row': 5,
                       'placeholder': '一般介護状況を入力してください。',}),
        }

    def clean(self):
        cleaned_data = super(KirokuCreateForm, self).clean()

        exec_date = cleaned_data.get("exec_date")
        day_night = cleaned_data.get("day_night")
        input_date = cleaned_data.get("date")
        input_time = cleaned_data.get("time")
        print(input_time)
        next_date = exec_date + timedelta(days=1)

        n_s_time = settings.NIKKIN_START_TIME
        y_s_time = settings.YAKIN_START_TIME

        if day_night == settings._NIKKIN:
            input_time = input_time or '12:00:00'
            workTimeF = datetime(year=exec_date.year, month=exec_date.month, day=exec_date.day, hour=n_s_time.hour)
            workTimeT = datetime(year=exec_date.year, month=exec_date.month, day=exec_date.day, hour=y_s_time.hour)
        else:
            input_time = input_time or '00:00:00'
            workTimeF = datetime(year=exec_date.year, month=exec_date.month, day=exec_date.day, hour=y_s_time.hour)
            workTimeT = datetime(year=next_date.year, month=next_date.month, day=next_date.day, hour=n_s_time.hour)

        input_dateTime = datetime.strptime(str(input_date) + ' '+ str(input_time), '%Y-%m-%d %H:%M:%S')

        if not(workTimeF <= input_dateTime < workTimeT):
            workTimeT = workTimeT - timedelta(minutes=1)
            self.add_error('date', '日時は%s～%sの範囲で入力してください。' % (workTimeF, workTimeT))
            # raise forms.ValidationError('日付のエラーだよ')

        return cleaned_data

class KirokuDeleteForm(forms.ModelForm):
    class Meta():
        model = Kiroku
        fields = ['riyosya', 'date', 'time', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'memo': forms.Textarea(
                attrs={'class': 'form-control form-control-sm col-12',
                       'row': 5,
                       'placeholder': '一般介護状況を入力してください。',}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['riyosya'].queryset = Riyosya.objects.filter(status=riyosya_status[0][0]).order_by('furigana')
