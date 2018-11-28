from django import forms
from ..models import Event, Riyosya, riyosya_status, ht_kbn, Staff

class EventForm(forms.ModelForm):
    class Meta():
        model = Event
        fields = ['date', 'knd', 'riyosya', 'time', 'ht_kbn', 'go_place', 'd_staff', 't_staff', 'naiyo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control col-3'}),
            'knd': forms.Select(
                    attrs={'class': 'form-control col-3',
                           'data-target': 'collapseExample',
                          }),
            'riyosya': forms.Select(attrs={'class': 'form-control col-8'}),
            'time': forms.TimeInput(attrs={'class': 'form-control col-3'}),
            'ht_kbn': forms.Select(attrs={'class': 'form-control col-2'}),
            'go_place': forms.Select(attrs={'class': 'form-control col-8'}),
            'd_staff': forms.Select(attrs={'class': 'form-control col-8'}),
            't_staff': forms.Select(attrs={'class': 'form-control col-8'}),
            'naiyo': forms.TextInput(attrs={'class': 'form-control col-4'}),
        }


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


        # self.fields['riyosya'].required = True
        # self.fields['riyosya'].queryset = Riyosya.objects.filter(status=)
