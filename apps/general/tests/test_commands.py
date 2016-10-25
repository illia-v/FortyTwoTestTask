from StringIO import StringIO
import sys

from django.db import models
from django.core.management import call_command
from django.test import TestCase


class TestPrintAllModels(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_models = models.get_models(include_auto_created=True)
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
        stdout_value = self.stdout.getvalue()
        for model in self.all_models:
            self.assertIn(
                'Model `%s` - %d instances' % (model.__name__,
                                               model.objects.count()),
                stdout_value, 'Should write names of models and the count of '
                'objects in every model to stdout'
            )

    def test_print_all_models_writes_to_stderr(self):
        """
        Ensures that `print_all_models` prints both names of models and
        the count of objects in every model to stderr
        """
        stderr_value = self.stderr.getvalue()
        for model in self.all_models:
            self.assertIn(
                'error: Model `%s` - %d instances' % (model.__name__,
                                                      model.objects.count()),
                stderr_value, 'Should write names of models and the count of '
                'objects in every model to stderr'
            )
