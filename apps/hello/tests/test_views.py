from django.test import TestCase


class TestHelloView(TestCase):
    """
    A test case for a view `HelloView`
    """
    def setUp(self):
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

    def test_hello_view_template_output(self):
        """
        Ensures that output of a `HelloView` teplate is valid
        """
        resopnse_content = self.response.content
        self.assertIn('Illia', resopnse_content,
                      "Person's first name should be in the template")
        self.assertIn('Volochii', resopnse_content,
                      "Person's last name should be in the template")
        self.assertIn('illia.volochii@gmail.com', resopnse_content,
                      "Person's email should be in the template")
