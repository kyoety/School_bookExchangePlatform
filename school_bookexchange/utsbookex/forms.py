from django import forms
from .models import Bookforsale, BeUser

class BookEditForm(forms.ModelForm):
    class Meta():
        model = Bookforsale
        exclude = ["bdate","buser"]
        labels = {
            "bimage":"",
            "bname":"Book Name:",
            "bqual":"Quality:",
            "bgrade":"Grade:",
            "bsubject":"Subject:",
            "bprice":"Price:",
            "bdescript":"Details (optional):"
        }
        QUAL_CHOICES = (
            ('Pristine','New/Pristine'),
            ('Great','Great'),
            ('Good','Good'),
            ('Average','Average'),
            ('Poor','Poor'),
            ('Bad','Bad'),
            ('Other','Other'),
        )
        GRADE_CHOICES = (
            ('F1','F1'),
            ('F2','F2'),
            ('M3','M3'),
            ('M4','M4'),
            ('S5','S5'),
            ('S6','S6'),
            ('Other','Other')
        )
        SUBJECT_CHOICES = (
            ('English','English'),
            ('French','French'),
            ('Economics','Economics'),
            ('Sciences','Sciences'),
            ('Spanish','Spanish'),
            ('Math','Math'),
            ('German','German'),
            ('Latin','Latin'),
            ('Other','Other'),
        )
        widgets = {'bimage' : forms.FileInput(),
                    'bqual' : forms.Select(choices=QUAL_CHOICES),
                    'bgrade' : forms.Select(choices=GRADE_CHOICES),
                    'bsubject' : forms.Select(choices=SUBJECT_CHOICES),
                    }

    def __init__(self, *args, **kwargs):
        super(BookEditForm, self).__init__(*args,**kwargs)
        self.fields['bname'].widget.attrs.update({'style' : 'class: inputform;'})
        self.fields['bimage'].widget.attrs.update({'style' : 'display: none;'})

class PrfEditForm(forms.ModelForm):
    class Meta():
        model = BeUser
        exclude = ["umail","uimage","udate"]
        labels = {
            "uname": "Name:",
            "ugrade": "Grade:",
            "upickup": "Prefered pickup location (Postal Code or School):",
        }
        GRADEE_CHOICES = (
            ('F1','F1'),
            ('F2','F2'),
            ('M3','M3'),
            ('M4','M4'),
            ('S5','S5'),
            ('S6','S6'),
        )
        widgets = {'ugrade' : forms.Select(choices=GRADEE_CHOICES)}
    def __init__(self, *args, **kwargs):
        super(PrfEditForm, self).__init__(*args, **kwargs)