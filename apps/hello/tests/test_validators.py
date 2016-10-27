import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now

from ..validators import validate_birth_date


class TestValidateBirthDate(TestCase):
    def test_validate_birth_date_with_valid_date(self):
        """
        Ensures that the validator `validate_birth_date` validates dates
        which are not in the future and were not more than 120 years ago
        """
        try:
            validate_birth_date(now().date())
            validate_birth_date(now().date().replace(year=now().year-100))
        except ValidationError:
            self.fail("Should accept valid dates")

    def test_validate_birth_date_with_future_date(self):
        """
        Ensures that the validator `validate_birth_date` does not
        validate dates which are in the future
        """
        future_date = now().date()+datetime.timedelta(days=1)
        with self.assertRaises(ValidationError,
                               msg="Should not accept future dates"):
            validate_birth_date(future_date)

    def test_validate_birth_date_with_too_old_date(self):
        """
        Ensures that the validator `validate_birth_date` does not
        validate dates which were more than 120 years ago
        """
        too_old_date = now().date().replace(year=now().year-200)
        with self.assertRaises(ValidationError,
                               msg="Should accept too old dates"):
            validate_birth_date(too_old_date)
