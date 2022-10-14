# std
from __future__ import annotations as _annotations
from typing import List as _List, Optional as _Opt, Union as _Union

# external
from jw_types import (
    Data as _Data,
    ObjectData as _ObjectData,
)
from jw_datatools import dict_utils as _dict_utils


class Config:

    def __init__(
            self,
            data: _Opt[_ObjectData] = None,
            name: _Opt[str] = None,
            prefix: _Opt[_Union[str, _List[str]]] = None,
    ):
        self._data: _ObjectData = data or {}
        self._name: _Opt[str] = name
        self._prefix: _List[str] = _dict_utils.normalize_keys(prefix)

    def get(self, keys: _Union[str, _List[str]], default: _Data = None) -> _Data:
        keys = self._prefix + _dict_utils.normalize_keys(keys)
        return _dict_utils.safeget(self._data, keys, default)

    def set(self, keys: _Union[str, _List[str]], value: _Data) -> Config:
        keys = self._prefix + _dict_utils.normalize_keys(keys)
        _dict_utils.safeset(self._data, keys, value)
        return self

    def sub(self, prefix: _Opt[_Union[str, _List[str]]] = None) -> Config:
        prefix = _dict_utils.normalize_keys(prefix)
        return Config(self._data, self._name, self._prefix + prefix)

    def unwrap(self) -> _ObjectData:
        return self._data
