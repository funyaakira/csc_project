from django import forms
from django.conf import settings
from ..models import Event, Riyosya, riyosya_status, ht_kbn, Staff

class EventForm(forms.ModelForm):
    class Meta():
        model = Event
        fields = ['date', 'knd', 'riyosya', 'time', 'ht_kbn', 'go_place', 'd_staff', 't_staff', 'naiyo']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control col-lg-3', 'readonly':'readonly'}),
            'knd': forms.Select(
                    attrs={'class': 'form-control col-lg-3',
                           'data-target': 'collapseExample',
                          }),
            'riyosya': forms.Select(attrs={'class': 'form-control col-lg-8'}),
            'time': forms.TimeInput(attrs={'class': 'form-control col-lg-3'}),
            'ht_kbn': forms.Select(attrs={'class': 'form-control col-lg-2'}),
            'go_place': forms.Select(attrs={'class': 'form-control col-lg-8'}),
            'd_staff': forms.Select(attrs={'class': 'form-control col-lg-8'}),
            't_staff': forms.Select(attrs={'class': 'form-control col-lg-8'}),
            'naiyo': forms.TextInput(attrs={'class': 'form-control col-lg-12'}),
        }


    def __init__(self, *args, **kwargs):
        event_knd_id = kwargs.pop('event_knd_id')
        super(EventForm, self).__init__(*args, **kwargs)

        if event_knd_id == settings._EVENT_KND_NYUSYO:
            self.fields['riyosya'].queryset = Riyosya.objects.filter(status=settings._RIYOSYA_STATUS_TAISYO).order_by('furigana')
        elif event_knd_id == settings._EVENT_KND_TAISYO:
            self.fields['riyosya'].queryset = Riyosya.objects.filter(status=settings._RIYOSYA_STATUS_NYUSYO).order_by('furigana')
        elif event_knd_id == settings._EVENT_KND_GAISYUTU:
            self.fields['riyosya'].queryset = Riyosya.objects.filter(status=settings._RIYOSYA_STATUS_NYUSYO).order_by('furigana')
        elif event_knd_id == settings._EVENT_KND_JUSIN:
            self.fields['riyosya'].queryset = Riyosya.objects.filter(status=settings._RIYOSYA_STATUS_NYUSYO).order_by('furigana')
