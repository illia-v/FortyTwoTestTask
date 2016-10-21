from django.forms import TextInput


class FormControlTextInput(TextInput):
    """
    A text input with a class `form-control` which is used by Bootstrap
    """
    def __init__(self, attrs={}):
        if attrs.get('class', None):
            attrs['class'] += ' form-control'
        else:
            attrs['class'] = 'form-control'
        attrs['required'] = 'true'

        super(FormControlTextInput, self).__init__(attrs)
