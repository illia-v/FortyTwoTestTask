"""
There are functions which create model instances
They are used in test cases to make code DRY
"""
from .. import models


def request():
    return models.Request.objects.create(url='/', method='GET')
