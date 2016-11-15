from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'msg-input',
                       'required': True, 'maxlength': 500,
                       'placeholder': 'Type your message here...'}
            )
        }
