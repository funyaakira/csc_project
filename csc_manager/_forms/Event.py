from django import forms
from ..models import Event, Riyosya

class EventForm(forms.ModelForm):
    class Meta():
        model = Event
        fields = ['date', 'knd', 'riyosya', 'time', 'ht_kbn', 'go_place', 'd_staff', 't_staff', 'naiyo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'knd': forms.Select(
                    attrs={'class': 'form-control form-control-sm col-3',
                           'onchange': 'this.form.submit();'
                          }),
            'riyosya': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'time': forms.TimeInput(attrs={'class': 'form-control form-control-sm col-4'}),
            'ht_kbn': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'go_place': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'd_staff': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            't_staff': forms.Select(attrs={'class': 'form-control form-control-sm col-8'}),
            'naiyo': forms.TextInput(attrs={'class': 'form-control form-control-sm col-4'}),
        }


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['riyosya'].required = True
        self.fields['riyosya'].queryset = Riyosya.objects.filter(taisyo_flg=False)
