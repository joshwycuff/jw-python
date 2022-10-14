# external
import pytest

# internal
from jw_datatools.data_view import DataView


def test_empty():
    assert DataView().data is None


def test_not_empty():
    assert DataView({}).data == {}


def test_not_empty_with_prefix():
    assert DataView({'x': 1}, 'x').data == {'x': 1}


def test_get_empty():
    assert DataView().get() is None


def test_get_not_empty():
    assert DataView({}).get() == {}


def test_get_not_empty_with_prefix():
    assert DataView({'x': 1}, 'x').get() == 1


def test_get_not_empty_with_key():
    assert DataView({'x': 1}).get('x') == 1


def test_with_keys_str():
    assert DataView({'x': {'y': 1}}).get('x.y') == 1


def test_with_keys_list():
    assert DataView({'x': {'y': 1}}).get(['x', 'y']) == 1


def test_set():
    data = DataView({})
    data.set('x', 1)
    assert data.data == {'x': 1}


def test_nested_set_with_str_keys():
    data = DataView({})
    data.set('x.y', 1)
    assert data.data == {'x': {'y': 1}}


def test_nested_set_with_list_keys():
    data = DataView({})
    data.set(['x', 'y'], 1)
    assert data.data == {'x': {'y': 1}}


def test_view_data():
    data = DataView({'x': {'y': 1}})
    view = data.view('x')
    assert view.data == {'x': {'y': 1}}


def test_view_get():
    data = DataView({'x': {'y': 1}})
    view = data.view('x')
    assert view.get() == {'y': 1}


def test_nested_view_get():
    data = DataView({'x': {'y': 1}})
    view = data.view('x.y')
    assert view.get() == 1


def test_set_empty():
    data = DataView()
    data.set(value={})
    assert data.data == {}
