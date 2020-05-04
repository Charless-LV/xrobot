from django  import forms
from .models import Task, Xperf, Perf

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'mode', 'device', 'description','status']



class XperfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', None)
        super(XperfForm, self).__init__(*args, **kwargs)
        print(self.mode)
        if not self.mode:
            self.fields['buff']= forms.CharField(
                required= False,
                widget=forms.TextInput(attrs={'type': 'hidden'})
            )
            self.fields['parallel']= forms.CharField(
                required= False,
                widget=forms.TextInput(attrs={'type': 'hidden'})
            )
            self.fields['interval']= forms.CharField(
                required= False,
                widget=forms.TextInput(attrs={'type': 'hidden'})
            )
            self.fields['seconds']= forms.CharField(
                required= False,
                widget=forms.TextInput(attrs={ 'type': 'hidden'})
            )
            #'class': 'form-control', 'id':'auto_mode', 'placeholder':'0',

    class Meta:
        model = Xperf
        fields = ['ip', 'port', 'buff', 'parallel','interval','seconds']
