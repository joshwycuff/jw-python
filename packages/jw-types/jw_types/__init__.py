# std
from __future__ import annotations as _annotations
from typing import (
    Dict as _Dict,
    List as _List,
    Union as _Union,
)

# types
NoneType = type(None)

AtomicData = _Union[NoneType, bool, str, int, float]
ObjectData = _Dict[str, 'JsonData']
ArrayData = _List['JsonData']
Data = _Union[AtomicData, ObjectData, ArrayData]


class _Null:

    @staticmethod
    def type() -> type(_Null):
        return _Null


null = _Null()
