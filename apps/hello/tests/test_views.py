import re

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from .model_instances import person_info
from ..models import PersonInfo
from ..views import HelloEditView


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


class TestHelloEditView(TestCase):
    """
    A test case for a view `HelloEditView`
    """
    def setUp(self):
        person_info()
        self.user = User.objects.create(username='test', password='testpswd')

    def test_hello_edit_view_basic(self):
        """
        Ensures that `HelloEditView` uses an appropriate template and
        authenticated users can get its response
        """
        request = RequestFactory().get('/')
        request.user = self.user
        response = HelloEditView.as_view()(request)

        self.assertTemplateUsed(response, 'hello/edit.html',
                                'Should use an appropriate template')
        self.assertEqual(response.status_code, 200,
                         'Should be callable by a registered user')

    def test_anonymous(self):
        """
        Ensures that `HelloEditView` is not accessed when user is not
        authenticated
        """
        response_for_anonymous = self.client.get("/edit_hello/")
        self.assertIn('login', response_for_anonymous.url,
                      'Should redirect to login')

    def test_hello_edit_view_template_output(self):
        """
        Ensures that output of a `HelloEditView` teplate is valid
        """
        request = RequestFactory().get('/')
        request.user = self.user
        response_content = HelloEditView.as_view()(request)._container[0]
        person = PersonInfo.objects.first()

        self.assertRegexpMatches(
            response_content,
            r'<input[^>.]* value="%s".*>' % person.first_name,
            "An input field for a person's first name should be in the "
            "template"
        )

        self.assertRegexpMatches(
            response_content,
            '<textarea[^>]*>%s<\\/textarea>' % (re.escape(person.bio)),
            "A textarea for person's bio should be in the template"
        )
