from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'msg-input',
                   'required': 'true',
                   'placeholder': 'Type your message here...'}
        ),
        max_length=500
    )
