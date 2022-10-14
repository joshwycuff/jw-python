# std
from __future__ import annotations as _annotations
import os as _os
import re as _re
from typing import (
    Callable as _Callable,
    IO as _IO,
    List as _L,
    Optional as _O,
    Union as _U,
)

# external
from jw_types import Data as _Data, NoneType as _NoneType

# internal
from jw_datatools.data_view import (
    OptKeysLike as _OptKeysLike,
    DataView as _DataView,
)

# types
_Dump = _Callable[[_Data, _IO], _NoneType]
_Load = _Callable[[_IO], _Data]
_OptDump = _O[_Dump]
_OptLoad = _O[_Load]


class PersistedData:
    _JSON_FILENAME_PATTERN = _re.compile(r'^.+\.json$')
    _TOML_FILENAME_PATTERN = _re.compile(r'^.+\.toml$')
    _YAML_FILENAME_PATTERN = _re.compile(r'^.+\.(yaml|yml)$')

    def __init__(
            self,
            filepath: str,
            data: _Data = None,
            prefix: _O[_U[str, _L[str]]] = None,
            auto_write: bool = False,
            dump: _OptDump = None,
            load: _OptLoad = None,
            binary: bool = False,
    ):
        self.filepath: str = filepath
        self.data_view: _DataView = _DataView(data, prefix)
        self._auto_write: bool = auto_write
        self.dump: _OptDump = dump
        self.load: _OptLoad = load
        self.binary: bool = binary

    @property
    def exists(self) -> bool:
        return _os.path.isfile(self.filepath)

    def base(self) -> PersistedData:
        return PersistedData(
            filepath=self.filepath,
            data=self.data_view.data,
            prefix=None,
            auto_write=self._auto_write,
            dump=self.dump,
            load=self.load,
        )

    def get(self, keys: _OptKeysLike = None, default: _Data = None) -> _Data:
        return self.data_view.get(keys, default)

    def set(self, keys: _OptKeysLike = None, value: _Data = None) -> PersistedData:
        self.data_view.set(keys, value)
        self.auto_write()
        return self

    def pop(self, keys: _OptKeysLike = None, default: _Data = None) -> PersistedData:
        self.data_view.pop(keys, default)
        self.auto_write()
        return self

    def view(self, prefix: _OptKeysLike = None) -> PersistedData:
        return PersistedData(
            filepath=self.filepath,
            data=self.data_view.data,
            prefix=self.data_view.keys(prefix),
            auto_write=self._auto_write,
            dump=self.dump,
            load=self.load,
        )

    def auto_write(self, auto_write: _O[bool] = None) -> PersistedData:
        if auto_write is not None:
            self._auto_write = auto_write
        if self._auto_write and self.dump is not None:
            self.write()
        return self

    def read(self) -> PersistedData:
        mode = 'rb' if self.binary else 'r'
        with open(self.filepath, mode) as fh:
            self.data_view.data = self.load(fh)
        return self

    def write(self) -> PersistedData:
        mode = 'wb' if self.binary else 'w'
        with open(self.filepath, mode) as fh:
            self.dump(self.data_view.data, fh)
        return self

    def as_json(self) -> PersistedData:
        import json
        self.load = json.load
        self.dump = json.dump
        return self

    def as_toml(self) -> PersistedData:
        import toml
        self.load = toml.load
        self.dump = toml.dump
        return self

    def as_yaml(self) -> PersistedData:
        import yaml
        self.load = yaml.load
        self.dump = yaml.dump
        return self

    def try_infer_type(self) -> PersistedData:
        if self.is_json_filename(self.filepath):
            self.as_json()
        elif self.is_toml_filename(self.filepath):
            self.as_toml()
        elif self.is_yaml_filename(self.filepath):
            self.as_yaml()
        return self

    @classmethod
    def json(
            cls,
            filepath: str,
            data: _Data = None,
            prefix: _O[_U[str, _L[str]]] = None,
            auto_write: bool = False,
    ):
        return cls(
            filepath=filepath,
            data=data,
            prefix=prefix,
            auto_write=auto_write,
        ).as_json().auto_write()

    @classmethod
    def toml(
            cls,
            filepath: str,
            data: _Data = None,
            prefix: _O[_U[str, _L[str]]] = None,
            auto_write: bool = False,
    ):
        return cls(
            filepath=filepath,
            data=data,
            prefix=prefix,
            auto_write=auto_write,
        ).as_toml().auto_write()

    @classmethod
    def yaml(
            cls,
            filepath: str,
            data: _Data = None,
            prefix: _O[_U[str, _L[str]]] = None,
            auto_write: bool = False,
    ):
        return cls(
            filepath=filepath,
            data=data,
            prefix=prefix,
            auto_write=auto_write,
        ).as_yaml().auto_write()

    @classmethod
    def new(
            cls,
            filepath: str,
            data: _Data = None,
            prefix: _O[_U[str, _L[str]]] = None,
            auto_write: bool = False,
            dump: _OptDump = None,
            load: _OptLoad = None,
            binary: bool = False,
    ) -> PersistedData:
        persisted_data = cls(
            filepath=filepath,
            data=data,
            prefix=prefix,
            auto_write=auto_write,
            dump=dump,
            load=load,
            binary=binary,
        )
        if dump is None or load is None:
            persisted_data.try_infer_type()
        persisted_data.auto_write()
        return persisted_data

    @classmethod
    def read_or_new(
            cls,
            filepath: str,
            data: _Data = None,
            auto_write: bool = False,
            prefix: _O[_U[str, _L[str]]] = None,
            dump: _OptDump = None,
            load: _OptLoad = None,
            binary: bool = False,
    ) -> PersistedData:
        if _os.path.isfile(filepath):
            persisted_data = cls(
                filepath=filepath,
                data=None,
                prefix=prefix,
                auto_write=auto_write,
                dump=dump,
                load=load,
                binary=binary,
            )
            if dump is None or load is None:
                persisted_data.try_infer_type()
            persisted_data.read()
        else:
            persisted_data = cls.new(
                filepath=filepath,
                data=data,
                prefix=prefix,
                auto_write=auto_write,
                dump=dump,
                load=load,
            )
        return persisted_data

    @classmethod
    def is_json_filename(cls, filepath: str) -> bool:
        return bool(_re.match(cls._JSON_FILENAME_PATTERN, filepath))

    @classmethod
    def is_toml_filename(cls, filepath: str) -> bool:
        return bool(_re.match(cls._TOML_FILENAME_PATTERN, filepath))

    @classmethod
    def is_yaml_filename(cls, filepath: str) -> bool:
        return bool(_re.match(cls._YAML_FILENAME_PATTERN, filepath))


class PersistedDataMixin:
    persisted_data: PersistedData

    def base(self) -> PersistedData:
        return self.persisted_data.base()

    def get(self, keys: _OptKeysLike = None, default: _Data = None) -> _Data:
        return self.persisted_data.get(keys, default)

    def set(self, keys: _OptKeysLike = None, value: _Data = None):
        self.persisted_data.set(keys, value)

    def pop(self, keys: _OptKeysLike = None, default: _Data = None):
        self.persisted_data.pop(keys, default)

    def view(self, prefix: _OptKeysLike = None) -> PersistedData:
        return self.persisted_data.view(prefix)
