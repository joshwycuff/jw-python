# std
from __future__ import annotations as _annotations
from typing import (
    List,
    Optional as Opt,
    Union,
)

# external
from jw_types import Data as _Data

# internal
from jw_datatools import dict_utils as _dict_utils

# types
Keys = List[str]
KeysLike = Union[str, Keys]
OptKeysLike = Opt[KeysLike]


class DataView:

    def __init__(
            self,
            data: _Data = None,
            prefix: OptKeysLike = None
    ):
        self.data: _Data = data
        self.prefix: Keys = _dict_utils.normalize_keys(prefix)

    def base(self) -> DataView:
        return DataView(self.data)

    def keys(self, keys: OptKeysLike = None) -> Keys:
        return self.prefix + _dict_utils.normalize_keys(keys)

    def get(self, keys: OptKeysLike = None, default: _Data = None) -> _Data:
        return _dict_utils.safeget(self.data, self.keys(keys), default)

    def set(self, keys: OptKeysLike = None, value: _Data = None) -> DataView:
        keys = self.keys(keys)
        if keys is None or keys == []:
            self.data = value
        else:
            _dict_utils.safeset(self.data, keys, value)
        return self

    def pop(self, keys: OptKeysLike = None, default: _Data = None) -> _Data:
        keys = self.keys(keys)
        if keys is None or keys == []:
            popped = self.data
            self.data = None
            return popped
        else:
            return _dict_utils.safepop(self.data, keys, default)

    def view(self, prefix: OptKeysLike = None) -> DataView:
        return DataView(data=self.data, prefix=self.keys(prefix))
