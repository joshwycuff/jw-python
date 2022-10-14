# internal
from jw_config import Config


def test_default_config():
    assert Config().unwrap() == {}


def test_empty_config():
    assert Config({}).unwrap() == {}


def test_non_empty_config():
    assert Config({'x': 1}).unwrap() == {'x': 1}


def test_get():
    assert Config({'x': 1}).get('x') == 1


def test_get_default_unset():
    assert Config({'x': 1}).get('y') is None


def test_get_default_set():
    assert Config({'x': 1}).get('y', 2) == 2


def test_set():
    assert Config({'x': 1}).set('x', 2).unwrap() == {'x': 2}


def test_sub():
    parent = Config({'a': {'b': 'c'}})
    child = parent.sub('a')
    assert child.get('b') == 'c'
