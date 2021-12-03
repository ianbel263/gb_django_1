from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_age(value):
    if value < 18:
        raise ValidationError(
            _('The age must be at least 18 years old.'),
            params={'value': value},
            code='age_mismatch'
        )
    return value
