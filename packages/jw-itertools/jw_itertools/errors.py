# external
from jw_errors import JwException as _JwException


class JwItertoolsException(_JwException):
    pass


class PowerIteratorException(JwItertoolsException):

    @classmethod
    def not_started(cls):
        raise PowerIteratorException('PowerIterator has not been started')


class NoPreviousValueException(PowerIteratorException):
    pass


class NoCurrentValueException(PowerIteratorException):
    pass


class NoNextValueException(PowerIteratorException):
    pass


no_previous_value_exception = NoPreviousValueException('')
no_current_value_exception = NoCurrentValueException('')
no_next_value_exception = NoNextValueException('')
