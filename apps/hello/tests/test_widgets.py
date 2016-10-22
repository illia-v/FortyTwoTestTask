from django.test import TestCase

from ..widgets import FormControlTextInput


class TestFormControlTextInput(TestCase):
    def test_form_control_text_input_with_defined_class(self):
        """
        Ensures that `TestFormControlTextInput` adds `form-control`
        class to other ones instead of replacing them
        """
        input_field = FormControlTextInput({'class': 'something'}).render(
            name='test', value='test'
        )
        self.assertEqual(
            input_field,
            '<input class="something form-control" name="test" '
            'required="true" type="text" value="test" />',
            'Should add `form-control` class to other classes'
        )

    def test_form_control_text_input_adds_class(self):
        """
        Ensures that `TestFormControlTextInput` adds `form-control`
        class
        """
        input_field = FormControlTextInput().render(name='test', value='test')
        self.assertEqual(
            input_field,
            '<input class="form-control" name="test" required="true" '
            'type="text" value="test" />',
            'Should add `form-control` class'
        )
