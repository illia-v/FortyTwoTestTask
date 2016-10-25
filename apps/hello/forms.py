from django import forms

from .models import PersonInfo
from .widgets import FormControlTextInput


class HelloEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HelloEditForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False

    class Meta:
        model = PersonInfo
        fields = '__all__'
        widgets = {
            'first_name': FormControlTextInput({'maxlength': 50}),
            'second_name': FormControlTextInput({'maxlength': 50}),
            'birth_date': FormControlTextInput({'maxlength': 50}),
            'bio': forms.Textarea({'class': 'form-control',
                                   'required': 'true',
                                   'rows': 5}),
            'photo': forms.FileInput({'id': 'photo-input',
                                      'accept': 'image/*'}),
            'email': forms.EmailInput({'class': 'form-control',
                                       'required': 'true'}),
            'jabber': forms.EmailInput({'class': 'form-control',
                                        'required': 'true'}),
            'skype': FormControlTextInput({'maxlength': 20}),
            'other_contacts': forms.Textarea({'class': 'form-control',
                                              'required': 'true',
                                              'rows': 5})
        }
