from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r"^\+[0-9]\d{7,14}$"
    message = _(
        "Phone number must be entered in a valid format.",
    )


phone_number_validators = [PhoneNumberValidator()]