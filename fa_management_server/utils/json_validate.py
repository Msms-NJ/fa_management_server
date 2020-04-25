# -*- coding: utf-8 -*-
from jsonschema import Draft7Validator, validators


def custom_validate(schema, instance):
    BaseVal = Draft7Validator

    # Build a new type checker
    def is_datetime(checker, inst):
        try:
            # datetime.datetime.strptime(inst, '%Y-%m-%d-%H.%M.%S.%f')
            return True
        except ValueError:
            return False

    date_check = BaseVal.TYPE_CHECKER.redefine(u'orderdatetime', is_datetime)

    # Build a validator with the new type checker
    Validator = validators.extend(BaseVal, type_checker=date_check)

    # Run the new Validator
    Validator(schema=schema).validate(instance)


# validate_with_datetime(schema, order)
