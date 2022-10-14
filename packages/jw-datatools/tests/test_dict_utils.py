# external
import pytest

# internal
from jw_datatools.errors import JwDataUtilsException
from jw_datatools.dict_utils import (
    normalize_keys,
    safeget,
    safeset,
    safepop,
)


def test_normalize_keys_default():
    assert normalize_keys() == []


def test_normalize_keys_none():
    assert normalize_keys(None) == []


def test_normalize_keys_empty_list():
    assert normalize_keys([]) == []


def test_normalize_keys_list():
    assert normalize_keys(['a', 'b']) == ['a', 'b']


def test_normalize_keys_str():
    assert normalize_keys('a.b') == ['a', 'b']


def test_normalize_keys_bad_input():
    with pytest.raises(JwDataUtilsException):
        normalize_keys(1)


def test_safeget():
    assert safeget({'a': {'b': 'c'}}, 'a.b') == 'c'


def test_safeget_default_unset():
    assert safeget({}, 'a.b') is None


def test_safeget_default_set():
    assert safeget({}, 'a.b', 'c') == 'c'


def test_safeset():
    assert safeset({}, 'a.b', 'c') == {'a': {'b': 'c'}}


def test_safeset_bad_input_1():
    with pytest.raises(JwDataUtilsException):
        safeset('a', 'a.b.', None)


def test_safeset_bad_input_2():
    with pytest.raises(JwDataUtilsException):
        safeset({'a': []}, 'a.b.', None)


def test_safeset_empty_keys():
    with pytest.raises(JwDataUtilsException):
        safeset({}, [], 'a')


def test_safepop():
    d = {'x': 1}
    result = safepop(d, 'x')
    assert d == {}
    assert result == 1


def test_safepop_nested():
    d = {'x': {'y': 2}}
    result = safepop(d, 'x.y')
    assert d == {'x': {}}
    assert result == 2


def test_safepop_default():
    d = {'x': 1}
    result = safepop(d, 'y')
    assert d == {'x': 1}
    assert result is None


def test_safepop_default_set():
    d = {'x': 1}
    result = safepop(d, 'y', 2)
    assert d == {'x': 1}
    assert result == 2


def test_safepop_none():
    d = None
    result = safepop(d, 'x')
    assert d is None
    assert result is None
