from django.test import TestCase

from .model_instances import person_info
from ..models import PersonInfo


class TestHelloView(TestCase):
    """
    A test case for a view `HelloView`
    """
    def setUp(self):
        person_info()
        self.response = self.client.get('/')

    def test_hello_view_basic(self):
        """
        Ensures that `HelloView` uses an appropriate template and
        everyone can get its response
        """
        self.assertTemplateUsed(self.response, 'hello/index.html',
                                'Should use an appropriate template')
        self.assertEqual(self.response.status_code, 200,
                         'Should be callable by anyone')

    def test_hello_view_returns_my_info(self):
        """
        Ensures that `HelloView` returns `PersonInfo` instance `my_info`
        in context
        """
        my_info = self.response.context_data['my_info']
        self.assertIs(type(my_info), PersonInfo, 'Should return a '
                      '`PersonInfo` instance `my_info` in context')

    def test_hello_view_template_output(self):
        """
        Ensures that output of a `HelloView` teplate is valid
        """
        resopnse_content = self.response.content
        person = PersonInfo.objects.first()
        self.assertIn(person.first_name, resopnse_content,
                      "Person's first name should be in the template")
        self.assertIn(person.second_name, resopnse_content,
                      "Person's last name should be in the template")
        self.assertIn(person.email, resopnse_content,
                      "Person's email should be in the template")
