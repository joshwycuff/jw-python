# std
from __future__ import annotations as _annotations


class JwException(Exception):
    pass


class JwValidationException(Exception):

    @classmethod
    def expect(
            cls,
            msg: str,
            condition: bool,
            exception_type: type(Exception),
    ):
        if not condition:
            raise exception_type(msg)


def expect(msg: str, condition: bool = False, exception_type: type(Exception) = JwValidationException):
    JwValidationException.expect(msg, condition, exception_type)
