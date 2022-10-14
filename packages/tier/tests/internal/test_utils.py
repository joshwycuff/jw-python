# internal
from tier.internal.dict_utils import safeget, safeset


def test_safeget_no_default():
    d = {}
    assert safeget(d, 'a.b') is None


def test_safeget_default():
    d = {}
    assert safeget(d, 'a.b', 'c') is 'c'


def test_safeget_nested_list():
    d = {'a': []}
    assert safeget(d, 'a.b') is None


def test_safeset():
    d = {}
    safeset(d, 'a.b', 'c')
    assert d == {'a': {'b': 'c'}}
