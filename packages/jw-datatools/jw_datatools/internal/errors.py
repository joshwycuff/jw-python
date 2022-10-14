# external
from jw_errors import expect as _expect

# internal
from jw_datatools.errors import JwDataUtilsException


def expect(
        msg: str,
        condition: bool = False,
        exception_type: type(Exception) = JwDataUtilsException,
):
    _expect(msg, condition, exception_type)
