from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_birth_date(birth_date):
    if now().date() < birth_date:
        raise ValidationError('You can not be born in the future')

    today_minus_120_years = now().date().replace(year=now().year-120)

    if birth_date < today_minus_120_years:
        raise ValidationError('You can not be more than 120 years old')
