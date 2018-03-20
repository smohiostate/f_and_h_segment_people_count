from functools import wraps
from flask_restful import reqparse

from ast import literal_eval
from inflection import camelize

from common.utils.responses import invalid_request
from common.utils.string_manipulation import  transform_to_underscore


def validate_input(InputValidatorClass):

    # We want to initialize this at initial run-time,
    # not during a RESTful call.
    validator = InputValidatorClass()

    def _validate_input(fn):
        """
        _validate_input() will parse the request and pass a validated
        and transformed input to the decorated function

        :param fn: The target function
        :return: A decorated function with the input_values dictionary injected
        """

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                validated_and_transformed_input = validator.validate_and_transform_input()
                return fn(*args, input_values=validated_and_transformed_input, **kwargs)
            except InputValidatorError as e:
                return invalid_request(message=e.message)

        return wrapper
    return _validate_input


# TODO: refactor this huge class
class InputValidator:
    # Assumptions:
    # InputValidator will be used on non-GET requests,
    # which means input keys will follow CAMELCASE.

    # Fields must be in snake case, to follow python naming conventions
    # the InputValidator will automatically transform input keys
    required_fields = []
    optional_fields = []

    # How to differentiate JSON fields
    class JSON(str):
        pass

    def __init__(self):
        assert type(self.required_fields) is list, "required_fields attribute must be a list"
        assert type(self.optional_fields) is list, "optional_fields attribute must be a list"

    def get_input_arguments(self):
        # Get required arguments
        required_parser = reqparse.RequestParser()
        for item in self.required_fields:
            argument_key = camelize(item, uppercase_first_letter=False)
            location = {} if not isinstance(item, InputValidator.JSON) else {'location': 'json'}
            required_parser.add_argument(argument_key, required=True,
                                         help="Input parameter {} is required.".format(
                                             camelize(argument_key, uppercase_first_letter=False)),
                                         **location)

        # Recurse and transform key names to snake case
        required_arguments = transform_to_underscore(dict(required_parser.parse_args()))

        # Get optional arguments
        optional_parser = reqparse.RequestParser()
        for item in self.optional_fields:
            argument_key = camelize(item, uppercase_first_letter=False)
            location = {} if not isinstance(item, InputValidator.JSON) else {'location': 'json'}
            optional_parser.add_argument(argument_key,
                                         help="Invalid input for {} parameter.".format(
                                             camelize(argument_key, uppercase_first_letter=False)),
                                         **location)

        # Recurse and transform key names to snake case
        optional_arguments = transform_to_underscore(dict(optional_parser.parse_args()))

        return required_arguments, optional_arguments

    def _is_input_valid(self):
        # Get input arguments from request
        required_arguments, optional_arguments = self.get_input_arguments()

        # By doing it this way,
        # we have a way to validate any arbitrary input data

        # Pass to our internal validator
        return self.is_input_valid(required_arguments, optional_arguments)

    @staticmethod
    def _safe_eval(value):
        try:
            return literal_eval(str(value))
        except SyntaxError:
            return value
        except ValueError:
            return value

    def is_input_valid(self, required_arguments, optional_arguments):
        # For each argument:
        # Get the argument's validator & run it on the argument's value
        # RAISE EXCEPTION on invalid values
        # return TRUE for perfect validation
        for argument in required_arguments:
            argument_value = transform_to_underscore(self._safe_eval(required_arguments.get(argument)))
            validator = getattr(self, '{}_validator'.format(argument), None)
            if callable(validator) and not validator(argument_value):
                raise InputValidatorError('{} is not valid.'.format(
                                             camelize(argument, uppercase_first_letter=False)))

        for argument in optional_arguments:
            argument_value = transform_to_underscore(self._safe_eval(optional_arguments.get(argument)))
            validator = getattr(self, '{}_validator'.format(argument), None)

            # Only check if a value has been passed.
            if argument_value is not None and callable(validator) and not validator(argument_value):
                raise InputValidatorError('{} is not valid.'.format(
                                             camelize(argument, uppercase_first_letter=False)))

        return True

    def transform_input(self, required_arguments, optional_arguments):
        # We will collect our output arguments
        output_arguments = dict()
        # For each argument:
        # Get the argument's transformer & run it on the argument's value
        for argument in required_arguments:
            argument_value = transform_to_underscore(self._safe_eval(required_arguments.get(argument)))
            transformer = getattr(self, '{}_transformer'.format(argument), None)
            output_arguments[argument] = transformer(argument_value) if callable(transformer) and argument_value is not None else argument_value

        for argument in optional_arguments:
            argument_value = transform_to_underscore(self._safe_eval(optional_arguments.get(argument)))
            transformer = getattr(self, '{}_transformer'.format(argument), None)
            output_arguments[argument] = transformer(argument_value) if callable(transformer) and argument_value is not None else argument_value

        return output_arguments

    def validate_and_transform_input(self):
        required_arguments, optional_arguments = self.get_input_arguments()
        if not self.is_input_valid(required_arguments, optional_arguments):
            raise InputValidatorError('Input parameters and values are invalid.')

        return self.transform_input(required_arguments, optional_arguments)


class InputValidatorError(Exception):
    pass

