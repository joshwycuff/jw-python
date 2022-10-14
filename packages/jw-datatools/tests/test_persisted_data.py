# std
import json

# external
import pytest
import toml
import yaml
from jw_types import Data
from jw_context.decorators import in_tmp_dir

# internal
from jw_datatools.persisted_data import PersistedData


def read(filepath: str, loader=json) -> Data:
    with open(filepath, 'r') as fh:
        if hasattr(loader, 'safe_load'):
            return loader.safe_load(fh)
        return loader.load(fh)


def write(filepath: str, data: Data, dumper=json) -> Data:
    with open(filepath, 'w') as fh:
        if hasattr(dumper, 'safe_dump'):
            return dumper.safe_dump(data, fh)
        return dumper.dump(data, fh)


@in_tmp_dir(dir='.')
def test_get():
    data = PersistedData.new('data.json', {'x': 1})
    assert data.get('x') == 1


@in_tmp_dir(dir='.')
def test_set():
    data = PersistedData.new('data.json', {'x': 1})
    data.set('x', 2)
    assert data.get('x') == 2


@in_tmp_dir(dir='.')
def test_view():
    data = PersistedData.new('data.json', {'x': {'y': 1}}, auto_write=True)
    view = data.view('x')
    view.set('y', 2)
    assert read('data.json', json) == {'x': {'y': 2}}


@in_tmp_dir(dir='.')
def test_exists():
    data = PersistedData.new('data.json')
    assert not data.exists
    data.write()
    assert data.exists


@in_tmp_dir(dir='.')
def test_set_auto_write_true():
    data = PersistedData.new('data.json', data={})
    assert not data.exists
    data.auto_write(True)
    assert data.exists


@in_tmp_dir(dir='.')
def test_set_auto_write_false():
    data = PersistedData.new('data.json', data={})
    assert not data.exists
    data.auto_write(False)
    assert not data.exists


@in_tmp_dir(dir='.')
def test_auto_write():
    data = PersistedData.new('data.json', data={}, auto_write=True)
    assert data.exists


@in_tmp_dir(dir='.')
def test_json():
    data = PersistedData.json('data.json', data={}, auto_write=True)
    assert read('data.json', json) == {}
    data.set('x', 1)
    assert read('data.json', json) == {'x': 1}


@in_tmp_dir(dir='.')
def test_json_inferred():
    data = PersistedData.new('data.json', data={}, auto_write=True)
    assert read('data.json', json) == {}
    data.set('x', 1)
    assert read('data.json', json) == {'x': 1}


@in_tmp_dir(dir='.')
def test_toml():
    data = PersistedData.toml('data.toml', data={}, auto_write=True)
    assert read('data.toml', toml) == {}
    data.set('x', 1)
    assert read('data.toml', toml) == {'x': 1}


@in_tmp_dir(dir='.')
def test_toml_inferred():
    data = PersistedData.new('data.toml', data={}, auto_write=True)
    assert read('data.toml', toml) == {}
    data.set('x', 1)
    assert read('data.toml', toml) == {'x': 1}


@in_tmp_dir(dir='.')
def test_yaml():
    data = PersistedData.yaml('data.yaml', data={}, auto_write=True)
    assert read('data.yaml', yaml) == {}
    data.set('x', 1)
    assert read('data.yaml', yaml) == {'x': 1}


@in_tmp_dir(dir='.')
def test_yaml_inferred():
    data = PersistedData.new('data.yaml', data={}, auto_write=True)
    assert read('data.yaml', yaml) == {}
    data.set('x', 1)
    assert read('data.yaml', yaml) == {'x': 1}


@in_tmp_dir(dir='.')
def test_read_exists():
    write('data.json', {'x': 1})
    data = PersistedData.read_or_new('data.json')
    assert data.get() == {'x': 1}


@in_tmp_dir(dir='.')
def test_read_or_new_exists():
    write('data.json', {'x': 1})
    data = PersistedData.read_or_new('data.json')
    assert data.get() == {'x': 1}


@in_tmp_dir(dir='.')
def test_read_or_new_not_exists():
    data = PersistedData.read_or_new('data.json', {'y': 2})
    assert data.get() == {'y': 2}
