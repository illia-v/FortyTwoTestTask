import logging
import sys

from django.core.management.base import BaseCommand
from django.db import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(stdout_handler)

stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.setLevel(logging.INFO)
stderr_handler.setFormatter(logging.Formatter('error: %(message)s'))
logger.addHandler(stderr_handler)


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        for model in models.get_models(include_auto_created=True):
            logger.info(
                'Model `%s` - %d instances' % (model.__name__,
                                               model.objects.count())
            )
