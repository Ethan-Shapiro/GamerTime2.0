from marshmallow import ValidationError


def is_ucsd_email(value):
    if value.split('@')[1] != 'ucsd.edu':
        raise ValidationError('Not valid UCSD email!')
