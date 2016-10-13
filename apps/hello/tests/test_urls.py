from django.test import TestCase
from django.core.urlresolvers import resolve, reverse


class TestHelloURLs(TestCase):
    def test_hello_view_url(self):
        """
        Ensures that a URL pattern name `hello` is valid and the pattern
        is resolved to `HelloView`
        """
        hello = resolve('/')

        self.assertEqual(reverse('hello'), '/', 'A view name `hello` should '
                         'be reversed to the URL `/`')
        self.assertEqual(hello.func.__name__, 'HelloView',
                         'Should be resolved to `HelloView`')
