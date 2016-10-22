from django.template import Context, Template
from django.test import TestCase

from hello.tests.model_instances import person_info


class TestEditLinkTemplateTag(TestCase):
    def setUp(self):
        self.person_info = person_info()

    def test_edit_link_return_link(self):
        """
        Ensures that a template tag `edit_link` returns valid result
        """
        template = Template('{% load edit_link %}'
                            '{% edit_link person %}')
        rendered = template.render(Context({'person': self.person_info}))
        edit_link = '/admin/hello/personinfo/%s/' % self.person_info.pk
        self.assertIn(edit_link, rendered, 'Should return an edit link')
