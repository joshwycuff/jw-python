# external
import pytest

# internal
from jw_errors import expect, JwValidationException


def test_expect_true():
    expect('should not fail', True)


def test_expect_false():
    with pytest.raises(JwValidationException):
        expect('should fail', False)


def test_expect_default():
    with pytest.raises(JwValidationException):
        expect('should fail')
