# external
from jw_errors import expect as _expect

# internal
from jw_config.errors import JwConfigException


def expect(msg: str, condition: bool = False, exception_type: type(Exception) = JwConfigException):
    _expect(msg, condition, exception_type)
