from StringIO import StringIO
import sys

from django.db import models
from django.core.management import call_command
from django.test import TestCase

from hello.models import PersonInfo


class TestPrintAllModels(TestCase):
    @classmethod
    def setUpClass(cls):
        # Transfer of stdout and stderr to variables
        cls.stdout = sys.stdout = StringIO()
        cls.stderr = sys.stderr = StringIO()

        call_command('print_all_models')

        # Assigning stdout and stderr their original values
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_print_all_models_writes_to_stdout(self):
        """
        Ensures that `print_all_models` prints both names of models and
        the count of objects in every model to stdout
        """
        self.assertIn(
            'Model `PersonInfo` - %d instances' % PersonInfo.objects.count(),
            self.stdout.getvalue(), 'Should write names of models and the '
            'count of objects in every model to stdout'
        )

    def test_print_all_models_writes_to_stderr(self):
        """
        Ensures that `print_all_models` prints both names of models and
        the count of objects in every model to stderr
        """
        self.assertIn(
            'Model `PersonInfo` - %d instances' % PersonInfo.objects.count(),
            self.stdout.getvalue(), 'Should write names of models and the '
            'count of objects in every model to stderr'
        )

    def test_print_all_models_writes_about_all_models(self):
        """
        Ensures that `print_all_models` prints information about all
        models of the project
        """
        self.assertEqual(
            self.stderr.getvalue().count('error:'),
            len(models.get_models(include_auto_created=True)),
            "Should write about all models"
        )
